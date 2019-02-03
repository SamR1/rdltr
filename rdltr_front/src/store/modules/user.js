import api from '../../api/defaultApi'
import authApi from '../../api/authApi'
import router from '../../router'

const state = {
  authToken: null,
  user: {},
  userErrorMessage: null
}

const getters = {
  isAuthenticated (state) {
    return state.authToken !== null
  },
  user (state) {
    return state.user
  },
  userErrorMessage (state) {
    return state.userErrorMessage
  }
}

const mutations = {
  authUser (state, token) {
    state.authToken = token
    state.userErrorMessage = null
  },
  clearUserData (state, token) {
    state.authToken = null
    state.user = {}
    state.userErrorMessage = null
  },
  updateErrorMsg (state, errMessage) {
    state.userErrorMessage = errMessage
  },
  userProfile (state, user) {
    state.user = user
  }
}

const actions = {
  checkUserAuth ({ commit, dispatch }) {
    if (window.localStorage.authToken) {
      commit('authUser', window.localStorage.authToken)
      dispatch('getUserProfile')
    }
  },
  getUserProfile ({ commit }) {
    authApi.get('auth/profile')
      .then(res => {
        if (res.data.status === 'success') {
          commit('userProfile', res.data.user)
        }
      })
      .catch(err => {
        if (err.response) {
          return commit('updateErrorMsg', err.response.data.message)
        }
        commit('updateErrorMsg', err.message
          ? err.message
          : `error on profile`)
      })
  },
  loginOrRegister ({ commit, dispatch }, data) {
    api.post(`/auth/${data.actionType}`, data.formData)
      .then(res => {
        if (res.data.status === 'success') {
          const token = res.data.auth_token
          window.localStorage.setItem('authToken', token)
          commit('authUser', token)
          dispatch('getUserProfile')
          router.replace('/')
        }
      })
      .catch(err => {
        if (err.response) {
          return commit('updateErrorMsg', err.response.data.message)
        }
        commit('updateErrorMsg', err.message
          ? err.message
          : `error on ${data.actionType}`)
      })
  },
  logout ({commit}) {
    commit('clearUserData')
    localStorage.removeItem('authToken')
    router.replace('/login')
  },
  // for now, only the password can be modified
  updateProfile  ({ commit, dispatch }, formData) {
    authApi.post(`/auth/profile/edit`, formData)
      .then(res => {
        if (res.data.status === 'success') {
          router.replace('/profile')
        }
      })
      .catch(err => {
        if (err.response) {
          return commit('updateErrorMsg', err.response.data.message)
        }
        commit('updateErrorMsg', err.message
          ? err.message
          : 'error on update password')
      })
  }
}

export default {
  state,
  getters,
  mutations,
  actions
}
