import Vue from 'vue'
import VueRouter from 'vue-router'

import AddArticle from '../components/articles/addArticle'
import Categories from '../components/settings/categories'
import Category from '../components/settings/category'
import DisplayArticle from '../components/articles/displayArticle'
import HomePage from '../components/home/home'
import NotFound from '../components/notFound'
import Settings from '../components/settings'
import UserDetail from '../components/user/userDetail'
import UserForm from '../components/auth/userForm'
import store from '../store'

Vue.use(VueRouter)

function checkAuth(to, from, next) {
  store.dispatch('checkUserAuth').then(() => {
    if (
      store.getters.isAuthenticated &&
      ['/login', '/register'].includes(to.path)
    ) {
      return next('/')
    }
    if (
      !store.getters.isAuthenticated &&
      !['/login', '/register'].includes(to.path)
    ) {
      return next('/login')
    }
  })
  next()
}

const routes = [
  {
    path: '/',
    component: HomePage,
    beforeEnter: checkAuth,
  },
  {
    path: '/register',
    component: UserForm,
    props: { actionType: 'register' },
    beforeEnter: checkAuth,
  },
  {
    path: '/login',
    component: UserForm,
    props: { actionType: 'login' },
    beforeEnter: checkAuth,
  },
  {
    path: '/profile',
    component: UserDetail,
    props: { actionType: 'viewProfile' },
    beforeEnter: checkAuth,
  },
  {
    path: '/profile/edit',
    component: UserDetail,
    props: { actionType: 'editProfile' },
    beforeEnter: checkAuth,
  },
  {
    path: '/articles/add',
    component: AddArticle,
    beforeEnter: checkAuth,
  },
  {
    path: '/articles/:id',
    component: DisplayArticle,
    name: 'articleDetail',
    beforeEnter: checkAuth,
  },
  {
    path: '/articles/page/:page',
    component: HomePage,
    name: 'articlesPage',
    beforeEnter: checkAuth,
  },
  {
    path: '/settings',
    component: Settings,
    beforeEnter: checkAuth,
  },
  {
    path: '/settings/categories/add',
    component: Category,
    name: 'addCategory',
    beforeEnter: checkAuth,
  },
  {
    path: '/settings/categories/:id',
    component: Category,
    name: 'editCategory',
    beforeEnter: checkAuth,
  },
  {
    path: '/settings/categories',
    component: Categories,
    beforeEnter: checkAuth,
  },
  { path: '*', component: NotFound },
]

export default new VueRouter({ mode: 'history', routes })
