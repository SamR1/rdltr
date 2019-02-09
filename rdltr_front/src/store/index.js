import Vue from 'vue'
import Vuex from 'vuex'

import articles from './modules/articles'
import categories from './modules/categories'
import user from './modules/user'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    selectedCategory: '',
    errorMessage: null,
  },
  mutations: {
    setCategory(state, selectedCategory) {
      state.selectedCategory = selectedCategory
    },
    setErrorMessage(state, errorMessage) {
      state.errorMessage = errorMessage
    },
  },
  actions: {
    updateSelectedCategory({ commit }, selectedCategory) {
      commit('setCategory', selectedCategory)
    },
    updateErrorMessage({ commit }, errorMessage) {
      commit('setErrorMessage', errorMessage)
    },
  },
  getters: {
    selectedCategory(state) {
      return state.selectedCategory
    },
    errorMessage(state) {
      return state.errorMessage
    },
  },
  modules: {
    articles,
    categories,
    user,
  },
})
