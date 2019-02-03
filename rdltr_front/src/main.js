import axios from 'axios'
import Vue from 'vue'

import App from './App'
import router from './router'

Vue.config.productionTip = false

axios.defaults.baseURL = 'http://localhost:5000/api'

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  render: h => h(App)
})
