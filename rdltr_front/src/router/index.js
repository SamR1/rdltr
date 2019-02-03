import Vue from 'vue'
import VueRouter from 'vue-router'

import HomePage from '../components/home/home.vue'
import NotFound from '../components/notFound'
import UserForm from '../components/auth/userForm.vue'
import store from '../store'

Vue.use(VueRouter)

function checkAuth (to, from, next) {
  store.dispatch('checkUserAuth').then(() => {
    if (store.getters.isAuthenticated && ['/login', '/register'].includes(to.path)) {
      console.log('redirect to home')
      return next('/')
    }
    if (!store.getters.isAuthenticated && !['/login', '/register'].includes(to.path)) {
      console.log('redirect to login')
      return next('/login')
    }
  })
  next()
}

const routes = [
  {
    path: '/',
    component: HomePage,
    beforeEnter: checkAuth
  },
  {
    path: '/register',
    component: UserForm,
    props: { actionType: 'register' },
    beforeEnter: checkAuth
  },
  {
    path: '/login',
    component: UserForm,
    props: { actionType: 'login' },
    beforeEnter: checkAuth
  },
  { path: '*', component: NotFound }
]

export default new VueRouter({ mode: 'history', routes })
