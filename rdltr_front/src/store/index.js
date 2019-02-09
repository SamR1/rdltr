import Vue from 'vue'
import Vuex from 'vuex'

import articles from './modules/articles'
import categories from './modules/categories'
import user from './modules/user'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    selectedCategory: '',
  },
  mutations: {
    updateCategory(state, selectedCategory) {
      state.selectedCategory = selectedCategory
    },
  },
  actions: {
    updateSelectedCategory({ commit }, selectedCategory) {
      commit('updateCategory', selectedCategory)
    },
  },
  getters: {
    selectedCategory(state) {
      return state.selectedCategory
    },
  },
  modules: {
    articles,
    categories,
    user,
  },
})
