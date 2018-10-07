// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
// import App from './App'
// import router from './router'
import Vuetify from '../node_modules/vuetify'
import VueRouter from '../node_modules/vue-router'
import 'vuetify/dist/vuetify.min.css'
import home from './Pages/App.vue'
import lumchan from './Pages/Doraemon.vue'

Vue.use(Vuetify, {
  theme: {
    primary: '#03A9F4',
    secondary: '#E1F5FE'
  }
})

Vue.use(VueRouter)

Vue.config.productionTip = false

const routes = [
  { path: '/bot/doraemon', component: lumchan }
]

const router = new VueRouter({
  routes
})

/* eslint-disable no-new */
new Vue({
  el: '#app',
  render: h => h(home),
  router: router
})
