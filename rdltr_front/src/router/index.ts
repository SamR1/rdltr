import { storeToRefs } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'

import { useUserStore } from '@/stores/user'
import { useAppStore } from '@/stores/app'
import AddArticleView from '@/views/AddArticleView.vue'
import ArticleView from '@/views/ArticleView.vue'
import BookmarkletView from '@/views/BookmarkletView.vue'
import HomeView from '@/views/HomeView.vue'
import ItemView from '@/views/ItemView.vue'
import ItemsView from '@/views/ItemsView.vue'
import NotFoundView from '@/views/NotFoundView.vue'
import ProfileView from '@/views/ProfileView.vue'
import SettingsView from '@/views/SettingsView.vue'
import UserFormView from '@/views/UserFormView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: HomeView
    },
    {
      path: '/register',
      name: 'Register',
      component: UserFormView,
      props: { actionType: 'register' }
    },
    {
      path: '/login',
      name: 'Login',
      component: UserFormView,
      props: { actionType: 'login' }
    },
    {
      path: '/profile',
      name: 'Profile',
      component: ProfileView,
      props: { actionType: 'view' }
    },
    {
      path: '/profile/edit',
      name: 'ProfileEdition',
      component: ProfileView,
      props: { actionType: 'edit' }
    },
    {
      path: '/articles/add',
      name: 'AddArticle',
      component: AddArticleView
    },
    {
      path: '/articles/:id',
      name: 'ArticleDetail',
      component: ArticleView
    },
    {
      path: '/articles/page/:page',
      name: 'Articles',
      component: HomeView
    },
    {
      path: '/bookmarklet',
      name: 'Bookmarklet',
      component: BookmarkletView
    },
    {
      path: '/settings',
      name: 'Settings',
      component: SettingsView
    },
    {
      path: '/settings/categories/add',
      name: 'AddCategory',
      component: ItemView,
      props: { itemType: 'categories' }
    },
    {
      path: '/settings/categories/:id/edit',
      name: 'EditCategory',
      component: ItemView,
      props: { itemType: 'categories' }
    },
    {
      path: '/settings/categories',
      name: 'CategoriesList',
      component: ItemsView,
      props: { itemType: 'categories' }
    },
    {
      path: '/settings/tags/add',
      name: 'AddTag',
      component: ItemView,
      props: { itemType: 'tags' }
    },
    {
      path: '/settings/tags/:id/edit',
      name: 'EditTag',
      component: ItemView,
      props: { itemType: 'tags' }
    },
    {
      path: '/settings/tags',
      name: 'TagsList',
      component: ItemsView,
      props: { itemType: 'tags' }
    },
    { path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFoundView }
  ]
})

router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore()
  const appStore = useAppStore()
  appStore.setErrorMessage(null)

  await userStore.checkUserAuth().then(() => {
    const { isAuthenticated } = storeToRefs(userStore)
    if (isAuthenticated.value && ['/login', '/register'].includes(to.path)) {
      return next({ name: 'Home' })
    }

    if (!isAuthenticated.value && !['/login', '/register'].includes(to.path)) {
      const path =
        to.path === '/'
          ? { path: '/login' }
          : { path: '/login', query: { from: to.fullPath } }
      return next(path)
    }

    return next()
  })
})

export default router
