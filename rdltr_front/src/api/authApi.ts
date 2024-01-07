import axios from 'axios'

import { useUserStore } from '@/stores/user'
import { storeToRefs } from 'pinia'
import { removeRequestIfPending } from '@/api/pending'
import { getApiUrl } from '@/utils'

const authApi = axios.create({ baseURL: getApiUrl() })

authApi.interceptors.request.use(
  (config) => {
    const userStore = useUserStore()
    const { authToken } = storeToRefs(userStore)
    if (authToken.value) {
      const auth = `Bearer ${authToken.value}`
      if (config.headers.Authorization !== auth) {
        config.headers.Authorization = auth
      }
    }
    return config
  },
  (error) => Promise.reject(error)
)
authApi.interceptors.response.use(
  (response) => {
    removeRequestIfPending(response.config)
    return response
  },
  (error) => {
    if (error.message !== 'canceled' && error.response) {
      removeRequestIfPending(error.response.config)
    }
    return Promise.reject(error)
  }
)

export default authApi
