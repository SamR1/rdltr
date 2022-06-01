import authApi from '../../api/authApi'
import router from '../../router'
import { handleError } from '@/utils'

const state = {}

const getters = {}

const mutations = {}

const actions = {
  addCategory({ commit, dispatch }, formData) {
    authApi
      .post('categories', formData)
      .then(() => {
        dispatch('getUserProfile')
        router.push('/settings/categories')
      })
      .catch((err) => handleError(commit, err, 'error on category creation'))
  },
  updateCategory({ commit, dispatch }, formData) {
    authApi
      .patch(`categories/${formData.id}`, formData)
      .then(() => {
        dispatch('getUserProfile')
        router.push('/settings/categories')
      })
      .catch((err) => handleError(commit, err, 'error on category update'))
  },
  deleteCategory({ commit, dispatch }, id) {
    authApi
      .delete(`categories/${id}`)
      .then((res) => {
        if (res.status === 204) {
          dispatch('getUserProfile')
        }
      })
      .catch((err) => handleError(commit, err, 'error on category deletion'))
  },
}

export default {
  state,
  getters,
  mutations,
  actions,
}
