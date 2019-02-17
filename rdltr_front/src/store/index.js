import Vue from 'vue'
import Vuex from 'vuex'

import articles from './modules/articles'
import categories from './modules/categories'
import tags from './modules/tags'
import user from './modules/user'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    selectedCategory: '',
    selectedTags: [],
    loading: false,
    errorMessage: null,
  },
  mutations: {
    setCategory(state, selectedCategory) {
      state.selectedCategory = selectedCategory
    },
    setErrorMessage(state, errorMessage) {
      state.errorMessage = errorMessage
      state.loading = false
    },
    setLoading(state, loading) {
      state.loading = loading
    },
    setTags(state, selectedTags) {
      state.selectedTags = selectedTags
    },
  },
  actions: {
    updateErrorMessage({ commit }, errorMessage) {
      commit('setErrorMessage', errorMessage)
    },
    updateLoading({ commit }, loading) {
      commit('setLoading', loading)
    },
    updateSelectedCategory({ commit }, selectedCategory) {
      commit('setCategory', selectedCategory)
    },
    updateSelectedTags({ commit }, selectedTags) {
      commit('setTags', selectedTags)
    },
  },
  getters: {
    loading(state) {
      return state.loading
    },
    selectedCategory(state) {
      return state.selectedCategory
    },
    selectedTags(state) {
      return state.selectedTags
    },
    errorMessage(state) {
      return state.errorMessage
    },
  },
  modules: {
    articles,
    categories,
    tags,
    user,
  },
})
