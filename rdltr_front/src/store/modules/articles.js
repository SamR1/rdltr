import authApi from '../../api/authApi'
import router from '../../router'

const state = {
  articles: [],
  articleErrorMessage: null
}

const getters = {
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
  }
}

export default {
  state,
  getters,
  mutations,
  actions
}
