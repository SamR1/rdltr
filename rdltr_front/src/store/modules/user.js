import api from '../../api/defaultApi'
import authApi from '../../api/authApi'
import router from '../../router'
import { handleError } from '../../utils'

const state = {
  authToken: null,
  user: {},
}

const getters = {
  isAuthenticated(state) {
    return state.authToken !== null
  },
  user(state) {
    return state.user
  },
  userCategories(state) {
    return state.user.categories
  },
}

const mutations = {
  authUser(state, token) {
    state.authToken = token
    state.userErrorMessage = null
  },
  clearUserData(state) {
    state.authToken = null
    state.user = {}
    state.userErrorMessage = null
  },
  userProfile(state, user) {
    state.user = user
  },
}

const actions = {
  checkUserAuth({ commit, dispatch }) {
    if (window.localStorage.authToken) {
      commit('authUser', window.localStorage.authToken)
      dispatch('getUserProfile')
    }
  },
  getUserProfile({ commit }) {
    authApi
      .get('auth/profile')
      .then(res => {
        if (res.data.status === 'success') {
          commit('userProfile', res.data.user)
        }
      })
      .catch(err => handleError(commit, err, 'error on profile'))
  },
  loginOrRegister({ commit, dispatch }, data) {
    api
      .post(`/auth/${data.actionType}`, data.formData)
      .then(res => {
        if (res.data.status === 'success') {
          const token = res.data.auth_token
          window.localStorage.setItem('authToken', token)
          commit('authUser', token)
          commit('setErrorMessage', '')
          dispatch('getUserProfile')
          router.replace('/')
        }
      })
      .catch(err => handleError(commit, err, `error on ${data.actionType}`))
  },
  logout({ commit }) {
    commit('clearUserData')
    localStorage.removeItem('authToken')
    router.replace('/login')
  },
  // for now, only the password can be modified
  updateProfile({ commit }, formData) {
    authApi
      .post(`/auth/profile/edit`, formData)
      .then(res => {
        if (res.data.status === 'success') {
          router.replace('/profile')
        }
      })
      .catch(err => handleError(commit, err, 'error on password update'))
  },
}

export default {
  state,
  getters,
  mutations,
  actions,
}
