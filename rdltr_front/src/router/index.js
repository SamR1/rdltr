import Vue from 'vue'
import VueRouter from 'vue-router'

import HomePage from '../components/home/home.vue'
import NotFound from '../components/NotFound'
import UserForm from '../components/auth/userForm.vue'
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
    }
  },
  {
    path: '/register',
    component: UserForm,
    props: { actionType: 'register' }
  },
  {
    path: '/login',
    component: UserForm,
    props: { actionType: 'login' }
  },
  { path: '*', component: NotFound }
]

export default new VueRouter({ mode: 'history', routes })
