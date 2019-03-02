import Vue from 'vue'
import Vuex from 'vuex'

import articles from './modules/articles'
import categories from './modules/categories'
import tags from './modules/tags'
import user from './modules/user'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    errorMessage: null,
    loading: false,
    onlyNotRead: false,
    selectedCategory: '',
    selectedTags: [],
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
    setOnlyNotRead(state, onlyNotRead) {
      state.onlyNotRead = onlyNotRead
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
    updateReadStatus({ commit }, onlyNotRead) {
      commit('setOnlyNotRead', onlyNotRead)
    },
    updateSelectedTags({ commit }, selectedTags) {
      commit('setTags', selectedTags)
    },
  },
  getters: {
    errorMessage(state) {
      return state.errorMessage
    },
    loading(state) {
      return state.loading
    },
    onlyNotRead(state) {
      return state.onlyNotRead
    },
    selectedCategory(state) {
      return state.selectedCategory
    },
    selectedTags(state) {
      return state.selectedTags
    },
  },
  modules: {
    articles,
    categories,
    tags,
    user,
  },
})
