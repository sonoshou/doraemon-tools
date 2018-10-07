<template>
  <div id="app">
    <v-app>
      <v-content id="kaiwa-content">
        <v-container fluid>
          <div>
            <div class="kaiwa">
              <figure class="kaiwa-img-left">
                <img src="../assets/img/icon_sonoshou.jpg" alt="no-img">
              </figure>
              <div class="kaiwa-text-left">
                <p class="kaiwa-text">
                  君の悩みごとを言ってごらん？<br>
                  例）将来が不安。お金がない。
                </p>
              </div>
            </div>
          </div>
          <!-- 繰り返し -->
          <div v-for="(item) in list" :key="item.id">
            <!-- 右からの吹き出し -->
            <div v-if="item.name=='User'"  class="kaiwa">
              <div class="kaiwa-text-right">
                <p class="kaiwa-text">
                  {{item.message}}
                </p>
              </div>
            </div>
            <!-- 左からの吹き出し -->
            <div v-if="item.name=='AI'" class="kaiwa">
              <figure class="kaiwa-img-left">
                <img src="../assets/img/icon_sonoshou.jpg" alt="no-img">
              </figure>
              <div class="kaiwa-text-left">
                <p class="kaiwa-text">
                  {{item.message}}
                </p>
              </div>
            </div>
          </div>
        </v-container>
      </v-content>

      <div>
        <v-container grid-list-md text-xs-center id="chat-container">
          <v-layout row wrap id="chat-layout">
            <v-flex xs9>
              <v-text-field
                label=""
                placeholder="メッセージを送る"
                single-line
                solo
                clearable
                autofocus
                v-model="message"
                @keydown=sendByEnter
              ></v-text-field>
            </v-flex>
            <v-flex xs3>
              <v-btn @click="sendMessage" id="chat-btn">送信</v-btn>
            </v-flex>
          </v-layout>
        </v-container>
      </div>
    </v-app>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'app',
  data () {
    return {
      list: [], // 名前とメッセージを格納
      name: '', // 名前
      message: '', // 送信メッセージ
      drawer: null
    }
  },
  methods: {
    sendByEnter () {
      if (window.event.keyCode === 13) {
        this.sendMessage()
      }
    },
    sendMessage () {
      // 空欄の場合は実行しない
      if (!this.message) return

      let list = {}
      list.name = 'User'
      list.message = this.message
      this.list.push(list)

      axios
        .get('http://13.115.119.149/api/v1/tools?q=' + this.message)
        .then(response => {
          let list = {}
          list.name = 'AI'
          list.message = response.data.data.response
          this.list.push(list)
        })
        .catch(error => console.log(error))
      this.name = ''
      this.message = ''
    }
  }
}
</script>

<style>
</style>
