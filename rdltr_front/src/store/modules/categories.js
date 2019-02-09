import authApi from '../../api/authApi'
import router from '../../router'
import { handleError } from '../../utils'

const state = {
  categories: [],
}

const getters = {}

const mutations = {}

const actions = {
  addCategory({ commit, rootState }, formData) {
    authApi
      .post('categories', formData)
      .then(() => {
        router.replace('/settings/categories')
      })
      .catch(err => handleError(commit, err, 'error on category creation'))
  },
  updateCategory({ commit, rootState }, formData) {
    authApi
      .patch(`categories/${formData.id}`, formData)
      .then(() => {
        router.replace('/settings/categories')
      })
      .catch(err => handleError(commit, err, 'error on category update'))
  },
  deleteCategory({ commit, dispatch, state }, id) {
    authApi
      .delete(`categories/${id}`)
      .then(res => {
        if (res.status === 204) {
          dispatch('getUserProfile')
        }
      })
      .catch(err => handleError(commit, err, 'error on category deletion'))
  },
}

export default {
  state,
  getters,
  mutations,
  actions,
}
