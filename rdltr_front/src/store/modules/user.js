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
  userTags(state) {
    return state.user.tags
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
  checkUserAuth({ commit, dispatch, getters }) {
    if (window.localStorage.authToken && !getters.isAuthenticated) {
      commit('authUser', window.localStorage.authToken)
      dispatch('getUserProfile')
    }
  },
  getUserProfile({ commit }) {
    authApi
      .get('auth/profile')
      .then(res => {
        if (res.data.status === 'success') {
          return commit('userProfile', res.data.user)
        }
        return handleError(commit, null)
      })
      .catch(err => handleError(commit, err))
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
          return router.push(data.redirect_url || '/')
        }
        return handleError(commit, null)
      })
      .catch(err => handleError(commit, err))
  },
  logout({ commit }) {
    commit('clearArticles')
    commit('clearUserData')
    localStorage.removeItem('authToken')
    router.push('/login')
  },
  // for now, only the password can be modified
  updateProfile({ commit }, formData) {
    authApi
      .post(`/auth/profile/edit`, formData)
      .then(res => {
        if (res.data.status === 'success') {
          return router.push('/profile')
        }
        return handleError(commit, null)
      })
      .catch(err => handleError(commit, err))
  },
}

export default {
  state,
  getters,
  mutations,
  actions,
}
