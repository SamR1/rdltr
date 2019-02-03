import Vue from 'vue'
import VueRouter from 'vue-router'

import HomePage from '../components/home/home.vue'
import LoginPage from '../components/auth/login.vue'
import NotFound from '../components/NotFound'
import RegisterPage from '../components/auth/register.vue'
import store from '../store'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    component: HomePage,
    beforeEnter (to, from, next) {
      if (store.state.user.authToken) {
        next()
      } else {
        next('/login')
      }
    } },
  { path: '/register', component: RegisterPage },
  { path: '/login', component: LoginPage },
  { path: '*', component: NotFound }
]

export default new VueRouter({ mode: 'history', routes })
