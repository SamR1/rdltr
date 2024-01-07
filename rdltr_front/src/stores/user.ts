import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { ComputedRef, Ref } from 'vue'

import authApi from '@/api/authApi'
import api from '@/api/defaultApi'
import type {
  ICategory,
  ILoginRegisterPayload,
  ITag,
  IUpdatePasswordFormData,
  IUser
} from '@/types'
import { handleError } from '@/utils'
import { useArticleStore } from '@/stores/articles'

export const useUserStore = defineStore('user', () => {
  const articleStore = useArticleStore()

  // state
  const authUser: Ref<IUser | null> = ref(null)
  const authToken: Ref<string | null> = ref(null)

  // getters
  const isAuthenticated: ComputedRef<boolean> = computed(
    () => authToken.value !== null
  )
  const userCategories: ComputedRef<ICategory[]> = computed(
    () => authUser.value?.categories || []
  )
  const userTags: ComputedRef<ITag[]> = computed(
    () => authUser.value?.tags || []
  )

  // actions
  async function checkUserAuth() {
    if (window.localStorage.authToken && !authToken.value) {
      authToken.value = window.localStorage.authToken
      await getUserProfile()
    }
  }

  async function getUserProfile() {
    authApi
      .get('auth/profile')
      .then((res) => {
        if (res.data.status === 'success') {
          authUser.value = res.data.user
        } else {
          handleError(null)
        }
      })
      .catch((err) => {
        if (err.response?.status === 401) {
          removeUserData()
        } else {
          handleError(err)
        }
      })
  }

  async function loginOrRegister(
    payload: ILoginRegisterPayload,
    actionType: string,
    redirect_url: string | null
  ) {
    api
      .post(`/auth/${actionType}`, payload)
      .then((res) => {
        if (res.data.status === 'success') {
          const token = res.data.auth_token
          window.localStorage.setItem('authToken', token)
          authToken.value = token
          authUser.value = res.data.user
          // @ts-ignore
          this.router.push(redirect_url || '/')
        } else {
          handleError(null)
        }
      })
      .catch((err) => handleError(err))
  }

  async function updatePassword(payload: IUpdatePasswordFormData) {
    authApi
      .post(`/auth/profile/edit`, {
        old_password: payload.oldPassword,
        new_password: payload.newPassword,
        new_password_conf: payload.confirmNewPassword
      })
      .then((res) => {
        if (res.data.status === 'success') {
          // @ts-ignore
          this.router.push('/profile')
        } else {
          handleError(null)
        }
      })
      .catch((err) => handleError(err))
  }

  function removeUserData() {
    localStorage.removeItem('authToken')
    authToken.value = null
    authUser.value = null
    articleStore.resetArticleStore()
    articleStore.emptyArticles()
  }

  function logout() {
    removeUserData()
    // @ts-ignore
    this.router.push('/login')
  }

  return {
    authToken,
    authUser,
    isAuthenticated,
    userCategories,
    userTags,
    checkUserAuth,
    getUserProfile,
    loginOrRegister,
    logout,
    removeUserData,
    updatePassword
  }
})
