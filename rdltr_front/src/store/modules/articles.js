import authApi from '../../api/authApi'
import router from '../../router'

const state = {
  article: {},
  articles: [],
  pagination: {},
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
  },
  pagination (state) {
    return state.pagination
  }
}

const mutations = {
  updateArticlesErrorMsg (state, errMessage) {
    state.articleErrorMessage = errMessage
  },
  getUserArticle (state, article) {
    state.article = article
  },
  getUserArticles (state, data) {
    state.articles = data.data
    state.pagination = data.pagination
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
  getArticles ({ commit, dispatch, state }, params) {
    let url = 'articles'
    if (params && params.page) {
      url += `?page=${params.page}`
    }
    authApi.get(url)
      .then(res => {
        if (res.data.status === 'success') {
          if (res.data.pagination.page > res.data.pagination.pages) {
            return router.replace(`/articles/page/${res.data.pagination.pages}`)
          }
          commit('getUserArticles', res.data)
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
  deleteArticle ({ commit, dispatch, state }, id) {
    authApi.delete(`articles/${id}`)
      .then(res => {
        if (res.status === 204) {
          dispatch('getArticles', {page: state.pagination.page})
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
