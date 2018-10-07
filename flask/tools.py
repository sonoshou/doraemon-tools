import csv, os, yaml, janome
from datetime import datetime
from gensim.models import word2vec
import numpy as np
from keras.models import load_model
from keras.models import Model
import tensorflow as tf
from janome.tokenizer import Tokenizer

class Tools:
    ITEM_CORPUS = '/data/v1/item_corpus.tsv'
    LOAD_MODEL = '/model/item_model.h5'
    W2V_MODEL = '/var/www/doraemon-tools/flask/model/wiki.model'
    MAX_WORDS_NUMBER = 10

    def __init__(self):
        # janomeの読み込み
        self.tokenizer = Tokenizer(mmap=True)

        # モデルの読み込み
        self.w2v_model = word2vec.Word2Vec.load(self.W2V_MODEL)

#        self.tagger = MeCab.Tagger("-Owakati -d{0}".format(self.config['path']['mecab']))

        self.ITEM_CORPUS = os.path.dirname(os.path.abspath(__file__)) + self.ITEM_CORPUS
        self.LOAD_MODEL = os.path.dirname(os.path.abspath(__file__)) + self.LOAD_MODEL

        self.load_file()
        self.analyze_morph()
        self.vectorize()
        self.load_model()
        self.calc_im_layer()

        self.graph = tf.get_default_graph()

    def load_file(self):
        csv_file = open(self.ITEM_CORPUS, "r", encoding="utf_8", errors="", newline="" )
        #リスト形式
        f = csv.reader(csv_file, delimiter="\t", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)

        self.q_raw_str = []
        self.a_raw_str = []
        self.i_raw_str = []
        self.c_raw_str = []

        for row in f:
            self.q_raw_str.append(row[0])
            self.a_raw_str.append(row[1])
            self.i_raw_str.append(row[2])
            self.c_raw_str.append(row[3])

    def analyze_morph(self):
        self.q_analyzed_str = []
        self.a_analyzed_str = []

        for raw_str in self.q_raw_str:
#            analyzed_str = self.tagger.parse(raw_str).strip().split(' ')
            analyzed_str = self.tokenizer.tokenize(raw_str, wakati=True)
            self.q_analyzed_str.append(analyzed_str)

        for raw_str in self.a_raw_str:
            analyzed_str = self.tokenizer.tokenize(raw_str, wakati=True)
            self.a_analyzed_str.append(analyzed_str)

    def vectorize(self):

        self.q_vector = []
        self.a_vector = []

        max_i = len(self.q_analyzed_str)

        for i in range(max_i):
            try:
                temp = self.w2v_model.wv[self.q_analyzed_str[i]]
                temp = self.w2v_model.wv[self.a_analyzed_str[i]]
            except KeyError:
                # print("KeyError:" + str(q_analyzed_str[i]) + " , " + str(a_analyzed_str[i]))
                self.q_raw_str[i] = "#delete_flag"
                self.a_raw_str[i] = "#delete_flag"
                continue
            self.q_vector.append(self.w2v_model.wv[self.q_analyzed_str[i]])
            self.a_vector.append(self.w2v_model.wv[self.a_analyzed_str[i]])

        self.q_raw_str = [raw_str for raw_str in self.q_raw_str if raw_str != "#delete_flag"]
        self.a_raw_str = [raw_str for raw_str in self.a_raw_str if raw_str != "#delete_flag"]

        # 1文を10個の単語ベクトルに分ける。
        self.MAX_WORDS_NUMBER = 10

        self.q_pad_vector = []
        self.a_pad_vector = []

        for vector in self.q_vector:
            vector_length = 10 if len(vector) > 10 else len(vector)
            pad_vector = np.pad(vector[0:self.MAX_WORDS_NUMBER], [(0,self.MAX_WORDS_NUMBER - vector_length),(0,0)], 'constant')
            self.q_pad_vector.append(pad_vector)

        for vector in self.a_vector:
            vector_length = 10 if len(vector) > 10 else len(vector)
            pad_vector = np.pad(vector[0:self.MAX_WORDS_NUMBER], [(0,self.MAX_WORDS_NUMBER - vector_length),(0,0)], 'constant')
            self.a_pad_vector.append(pad_vector)

    def load_model(self):
        # load model
        self.base_model = load_model(self.LOAD_MODEL)

        # numpy形式に変換
        self.q_np_array = np.array(self.q_pad_vector)
        self.a_good_np_array = np.array(self.a_pad_vector)

    def calc_im_layer(self):
        # model.input
        intermediante_layer_model = Model(inputs=self.base_model .get_input_at(0), outputs=self.base_model .get_layer("q_dense").output)
        self.q_predict = intermediante_layer_model.predict([self.q_np_array, self.a_good_np_array])

        intermediante_layer_model = Model(inputs=self.base_model .get_input_at(0), outputs=self.base_model .get_layer("a_dense").output)
        self.a_predict = intermediante_layer_model.predict([self.q_np_array, self.a_good_np_array])

    def response(self, input_str):
        # 1. 形態素解析
        analyzed_str = self.tokenizer.tokenize(input_str, wakati=True)

        # 2. ベクトル化
        input_vector = self.w2v_model.wv[analyzed_str]

        # 3. 0穴埋め
        vector_length = 10 if len(input_vector) > 10 else len(input_vector)
        input_pad_vector = np.pad(input_vector[0:self.MAX_WORDS_NUMBER], [(0,self.MAX_WORDS_NUMBER - vector_length),(0,0)], 'constant')

        # <tensor> is not an element of this の対策
        # https://qiita.com/itisyuu/items/7c9d7ff43b3936704918
        with self.graph.as_default():
            intermediante_layer_model = Model(inputs=self.base_model .get_layer("q_inputs").input, outputs=self.base_model .get_layer("q_dense").output)
            input_pad_vector.resize(1,10,100) # 学習時は複数のセットで学習したが、今回は1つのセットなので、resizeをして入力モデルの形式に合わせている。
            input_predict = intermediante_layer_model.predict(input_pad_vector)
            input_predict = input_predict[0] # 複数セットから１つのセットに戻す

        cos_sim_results = []

        for predict in self.a_predict:
            cos_sim_results.append(self.cos_sim(input_predict, predict))

        cos_sim_results = np.array(cos_sim_results)

        return self.i_raw_str[cos_sim_results.argmax()], self.c_raw_str[cos_sim_results.argmax()], str(cos_sim_results.max())

    def cos_sim(self, v1, v2):
        return (np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
