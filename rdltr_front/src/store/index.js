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
    errorMessage: null,
  },
  mutations: {
    setCategory(state, selectedCategory) {
      state.selectedCategory = selectedCategory
    },
    setErrorMessage(state, errorMessage) {
      state.errorMessage = errorMessage
    },
    setTags(state, selectedTags) {
      state.selectedTags = selectedTags
    },
  },
  actions: {
    updateErrorMessage({ commit }, errorMessage) {
      commit('setErrorMessage', errorMessage)
    },
    updateSelectedCategory({ commit }, selectedCategory) {
      commit('setCategory', selectedCategory)
    },
    updateSelectedTags({ commit }, selectedTags) {
      commit('setTags', selectedTags)
    },
  },
  getters: {
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
