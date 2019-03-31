import axios from 'axios'
import store from '../store'
import { getApiUrl } from '../utils'

const authApi = axios.create({
  baseURL: getApiUrl(),
})

authApi.interceptors.request.use(
  config => {
    if (store.state.user.authToken) {
      const auth = `Bearer ${store.state.user.authToken}`
      if (config.headers.Authorization !== auth) {
        config.headers.Authorization = `Bearer ${store.state.user.authToken}`
      }
    }
    return config
  },
  error => Promise.reject(error)
)

export default authApi
