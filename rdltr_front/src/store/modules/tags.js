import authApi from '../../api/authApi'
import router from '../../router'
import { handleError } from '@/utils'

const state = {}

const getters = {}

const mutations = {}

const actions = {
  addTag({ commit, dispatch }, formData) {
    authApi
      .post('tags', formData)
      .then(() => {
        dispatch('getUserProfile')
        router.push('/settings/tags')
      })
      .catch((err) => handleError(commit, err, 'error on tag creation'))
  },
  updateTag({ commit, dispatch }, formData) {
    authApi
      .patch(`tags/${formData.id}`, formData)
      .then(() => {
        dispatch('getUserProfile')
        router.push('/settings/tags')
      })
      .catch((err) => handleError(commit, err, 'error on tag update'))
  },
  deleteTag({ commit, dispatch }, id) {
    authApi
      .delete(`tags/${id}`)
      .then((res) => {
        if (res.status === 204) {
          dispatch('getUserProfile')
        }
      })
      .catch((err) => handleError(commit, err, 'error on tag deletion'))
  },
}

export default {
  state,
  getters,
  mutations,
  actions,
}
