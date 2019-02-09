import Vue from 'vue'
import VueRouter from 'vue-router'

import AddArticle from '../components/articles/articleAdd'
import DisplayArticle from '../components/articles/articleDisplay'
import HomePage from '../components/home/home'
import Item from '../components/common/item'
import Items from '../components/common/items'
import NotFound from '../components/notFound'
import Settings from '../components/settings'
import UserDetail from '../components/user/userDetail'
import UserForm from '../components/user/userForm'
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
    component: Item,
    name: 'addCategory',
    props: { itemType: 'categories' },
    beforeEnter: checkAuth,
  },
  {
    path: '/settings/categories/:id/edit',
    component: Item,
    name: 'editCategory',
    props: { itemType: 'categories' },
    beforeEnter: checkAuth,
  },
  {
    path: '/settings/categories',
    component: Items,
    props: { itemType: 'categories' },
    beforeEnter: checkAuth,
  },
  {
    path: '/settings/tags/add',
    component: Item,
    name: 'addTag',
    props: { itemType: 'tags' },
    beforeEnter: checkAuth,
  },
  {
    path: '/settings/tags/:id/edit',
    component: Item,
    name: 'editTag',
    props: { itemType: 'tags' },
    beforeEnter: checkAuth,
  },
  {
    path: '/settings/tags',
    component: Items,
    props: { itemType: 'tags' },
    beforeEnter: checkAuth,
  },
  { path: '*', component: NotFound },
]

export default new VueRouter({ mode: 'history', routes })
