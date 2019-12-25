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

const routes = [
  {
    path: '/',
    component: HomePage,
    name: 'home',
  },
  {
    path: '/register',
    component: UserForm,
    props: { actionType: 'register' },
  },
  {
    path: '/login',
    component: UserForm,
    props: { actionType: 'login' },
  },
  {
    path: '/profile',
    component: UserDetail,
    props: { actionType: 'viewProfile' },
  },
  {
    path: '/profile/edit',
    component: UserDetail,
    props: { actionType: 'editProfile' },
  },
  {
    path: '/articles/add',
    component: AddArticle,
  },
  {
    path: '/articles/:id',
    component: DisplayArticle,
    name: 'articleDetail',
  },
  {
    path: '/articles/page/:page',
    component: HomePage,
    name: 'articlesPage',
  },
  {
    path: '/settings',
    component: Settings,
  },
  {
    path: '/settings/categories/add',
    component: Item,
    name: 'addCategory',
    props: { itemType: 'categories' },
  },
  {
    path: '/settings/categories/:id/edit',
    component: Item,
    name: 'editCategory',
    props: { itemType: 'categories' },
  },
  {
    path: '/settings/categories',
    component: Items,
    props: { itemType: 'categories' },
  },
  {
    path: '/settings/tags/add',
    component: Item,
    name: 'addTag',
    props: { itemType: 'tags' },
  },
  {
    path: '/settings/tags/:id/edit',
    component: Item,
    name: 'editTag',
    props: { itemType: 'tags' },
  },
  {
    path: '/settings/tags',
    component: Items,
    props: { itemType: 'tags' },
  },
  { path: '*', component: NotFound },
]

const router = new VueRouter({ mode: 'history', routes })

router.beforeEach((to, from, next) => {
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
      const path =
        to.path === '/'
          ? { path: '/login' }
          : { path: '/login', query: { from: to.path } }
      next(path)
    }
  })
  next()
})

export default router
