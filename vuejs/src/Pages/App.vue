<template>
  <div id="app">
    <v-app>
      <v-navigation-drawer fixed v-model="drawer" app>
        <v-list dense>

          <v-list-group
          prepend-icon="android"
          value="true"
          >
            <v-list-tile slot="activator">
              <v-list-tile-title>ボット一覧</v-list-tile-title>
            </v-list-tile>

            <v-list-tile class="bot-icon"
              v-for="(bot, i) in bots"
              :key="i"
              @click="transitionPage(i)"
            >
              <v-list-tile-title v-text="bot[0]"></v-list-tile-title>
              <v-list-tile-action>
                <v-icon v-text="bot[1]"></v-icon>
              </v-list-tile-action>
            </v-list-tile>
          </v-list-group>
        </v-list>
      </v-navigation-drawer>
      <v-toolbar fixed app id="chat-toolbar">
        <v-toolbar-side-icon @click.stop="drawer = !drawer"></v-toolbar-side-icon>
        <v-toolbar-title>何か道具出して？</v-toolbar-title>
      </v-toolbar>

      <v-fade-transition mode="out-in">
        <router-view></router-view>
      </v-fade-transition>

    </v-app>
  </div>
</template>

<script>
export default {
  name: 'app',
  data () {
    return {
      drawer: null,
      bots: [
        ['ドラえもん', 'fa-female', '/#/bot/doraemon/']
      ]
    }
  },
  created () {
  },
  methods: {
    transitionPage (i) {
      window.location.href = this.bots[i][2]
    }
  }
}
</script>

<style>
/*——————–
 吹き出しを作る
——————–*/
/* 全体のスタイル */
.kaiwa {
  margin-bottom: 25px;
  padding-bottom: 25px;
}
/* 左画像 */
.kaiwa-img-left {
  margin: 0;
  float: left;
  width: 60px;
  height: 60px;
  margin-right: -70px;
}
/* 右画像 */
.kaiwa-img-right {
  margin: 0;
  float: right;
  width: 60px;
  height: 60px;
  margin-left: -70px;
}
.kaiwa figure img {
  width: 100%;
  height: 100%;
  border: 1px solid #707070;
  border-radius: 50%;
  margin: 0;
}
/* 画像の下のテキスト */
.kaiwa-img-description {
  padding: 5px 0 0;
  font-size: 10px;
  text-align: center;
  position: relative;
  bottom: 15px;
}
/* 左からの吹き出しテキスト */
.kaiwa-text-left {
  position: relative;
  margin-left: 80px;
  padding: 10px;
  border-radius: 10px;
  background-color: #fff;
  margin-right: 12%;
  float: left;
}
/* 右からの吹き出しテキスト */
.kaiwa-text-right {
  position: relative;
  padding: 10px;
  border-radius: 10px;
  color: #fff;
  background-color: #03A9F4;
  margin-left: 12%;
  float: right;
}
p.kaiwa-text {
  margin: 0 0 20px;
}
p.kaiwa-text:last-child {
  margin-bottom: 0;
}
/* 左の三角形を作る */
.kaiwa-text-left:before {
  position: absolute;
  content: '';
  border: 10px solid transparent;
  top: 15px;
  left: -20px;
}
.kaiwa-text-left:after {
  position: absolute;
  content: '';
  border: 10px solid transparent;
  border-right: 10px solid #fff;
  top: 15px;
  left: -19px;
}
/* 右の三角形を作る */
.kaiwa-text-right:before {
  position: absolute;
  content: '';
  border: 10px solid transparent;
  top: 15px;
  right: -20px;
}
.kaiwa-text-right:after {
  position: absolute;
  content: '';
  border: 10px solid transparent;
  border-left: 10px solid #03A9F4;
  top: 15px;
  right: -19px;
}
/* 回り込み解除 */
.kaiwa:after,.kaiwa:before {
  clear: both;
  content: "";
  display: block;
}

/* テキストエリア、送信ボタン④ */

#bms-send-message{
    width: calc(100% - 75px);/*常に送信ボタンの横幅を引いたサイズに動的に計算*/
    line-height: 16px;
    height: 48px;

}
#bms-send-btn {
    width: 50px;
    height: 48px;
    font-size: 16px;
    line-height: 3em;
    float: right;/*bms_sendに対して右寄せ*/
    color: #fff;
    font-weight: bold;
    /* text-align: center;文字をボタン中央に表示 */
    box-sizing: border-box;/*paddingとborderの要素の高さと幅の影響をなくす（要素に高さと幅を含める）*/
}

/* ナビゲーション */
#chat-toolbar {
  background-color: #03A9F4;
  color: #fff;
}

#chat-toolbar .v-btn{
  color: #fff;
}

.bot-icon .v-icon {
  margin: auto;
}

/* チャットの背景 */
#app {
  background-color: #E1F5FE;
}

/* チャット書き込みボタン */
#chat-btn {
  margin: 0;
  height: 48px;
  width: 100%;
  background-color: #444243;
  color: #fff;
}

#chat-container {
  margin: 1px 0;
  padding: 0;
  position: fixed;
  bottom: 0;
  width: 100%;
  max-width: none;
}

@media screen and (min-width: 1264px) {
  /* 1264px以上の場合 */
  #chat-container {
    padding-left: 300px
  }
}

#chat-layout .flex{
  padding: 0;
}

#chat-layout .v-messages {
  min-height: 0;
}

#chat-layout .v-input__slot{
  margin: 0;
}

#chat-layout .v-text-field__details{
  margin: 0;
  padding: 0;
}

#chat-layout{
  margin: 0;
}

</style>
