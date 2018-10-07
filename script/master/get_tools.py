import urllib.request as req
import json, os, yaml

with open(os.path.dirname(os.path.abspath(__file__)) + '/config.yml', 'r', encoding='utf-8') as yml:
    config = yaml.load(yml)

res = req.urlopen(config['url']['spread_sheet'])
html = res.read().decode('utf-8')
json_obj = json.loads(html)

write_str = ""
for row in json_obj:
    if not row[3] == "":
        write_str += row[0] + '\t' + row[3] + '\t' + row[4] + '\t' + row[5] + '\n'

# ファイル書き込み
path_w = os.getcwd() + "/script/data/selected_item_list.tsv"

with open(path_w, mode='w') as f:
    f.write(write_str)
