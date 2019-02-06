import Vue from 'vue'
import VueRouter from 'vue-router'

import AddArticle from '../components/articles/addArticle'
import displayArticle from '../components/articles/displayArticle'
import HomePage from '../components/home/home'
import NotFound from '../components/notFound'
import UserDetail from '../components/user/userDetail'
import UserForm from '../components/auth/userForm'
import store from '../store'

Vue.use(VueRouter)

function checkAuth (to, from, next) {
  store.dispatch('checkUserAuth').then(() => {
    if (store.getters.isAuthenticated && ['/login', '/register'].includes(to.path)) {
      return next('/')
    }
    if (!store.getters.isAuthenticated && !['/login', '/register'].includes(to.path)) {
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
  {
    path: '/profile',
    component: UserDetail,
    props: { actionType: 'viewProfile' },
    beforeEnter: checkAuth
  },
  {
    path: '/profile/edit',
    component: UserDetail,
    props: { actionType: 'editProfile' },
    beforeEnter: checkAuth
  },
  {
    path: '/articles/add',
    component: AddArticle,
    beforeEnter: checkAuth
  },
  {
    path: '/articles/:id',
    component: displayArticle,
    name: 'articleDetail',
    beforeEnter: checkAuth
  },
  { path: '*', component: NotFound }
]

export default new VueRouter({ mode: 'history', routes })
