import authApi from '../../api/authApi'
import router from '../../router'

const state = {
  article: {},
  articles: [],
  articleErrorMessage: null
}

const getters = {
  article (state) {
    return state.article
  },
  articles (state) {
    return state.articles
  },
  articleErrorMessage (state) {
    return state.articleErrorMessage
  }
}

const mutations = {
  updateArticlesErrorMsg (state, errMessage) {
    state.articleErrorMessage = errMessage
  },
  getUserArticle (state, article) {
    state.article = article
  },
  getUserArticles (state, articles) {
    state.articles = articles
  }
}

const handleError = (commit, err, msg) => {
  if (err.response) {
    return commit('updateArticlesErrorMsg', err.response.data.message)
  }
  return commit('updateArticlesErrorMsg', err.message
    ? err.message
    : msg)
}

const actions = {
  getArticle ({ commit }, id) {
    authApi.get(`articles/${id}`)
      .then(res => {
        if (res.data.status === 'success') {
          commit('getUserArticle', res.data.data[0])
        }
      })
      .catch(err => handleError(commit, err, 'error on articles fetch'))
  },
  getArticles ({ commit }) {
    authApi.get('articles')
      .then(res => {
        if (res.data.status === 'success') {
          commit('getUserArticles', res.data.data)
        }
      })
      .catch(err => handleError(commit, err, 'error on articles fetch'))
  },
  addArticle ({ commit }, formData) {
    authApi.post('articles', formData)
      .then(res => {
        if (res.data.status === 'success') {
          router.replace('/')
        }
      })
      .catch(err => handleError(commit, err, 'error on article add'))
  },
  deleteArticle ({ commit, dispatch }, id) {
    authApi.delete(`articles/${id}`)
      .then(res => {
        if (res.status === 204) {
          dispatch('getArticles')
        }
      })
      .catch(err => handleError(commit, err, 'error on article deletion'))
  }
}

export default {
  state,
  getters,
  mutations,
  actions
}
