import axios from 'axios'
import store from '../store'

const authApi = axios.create({
  baseURL: 'http://localhost:5000/api'
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
