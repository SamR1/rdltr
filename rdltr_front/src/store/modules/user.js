import api from '../../api/defaultApi'

const state = {
  user: {},
  isAuthenticated: false
}

const getters = {}

const mutations = {}

const actions = {
  login ({ commit, dispatch }, formData) {
    api.post('/auth/login', formData)
      .then(res => console.log(res))
      .catch(err => console.error(err))
  },
  register ({ commit, dispatch }, formData) {
    api.post('/auth/register', formData)
      .then(res => console.log(res))
      .catch(err => console.error(err))
  }
}

export default {
  state,
  getters,
  mutations,
  actions
}
