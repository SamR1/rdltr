import authApi from '../../api/authApi'
import router from '../../router'
import { handleError } from '../../utils'

const state = {
  article: {},
  articles: [],
  pagination: {},
  query: '',
}

const getters = {
  article(state) {
    return state.article
  },
  articles(state) {
    return state.articles
  },
  pagination(state) {
    return state.pagination
  },
  query(state) {
    return state.query
  },
}

const mutations = {
  getUserArticle(state, article) {
    state.article = article
  },
  getUserArticles(state, data) {
    state.articles = data.data
    state.pagination = data.pagination
  },
  updateQuery(state, query) {
    state.query = query
  },
  clearArticles(state) {
    state.article = {}
    state.articles = []
    state.pagination = {}
  },
}

const actions = {
  addArticle({ commit, dispatch }, formData) {
    dispatch('updateLoading', true)
    authApi
      .post('articles', formData)
      .then(res => {
        if (res.data.status === 'success') {
          dispatch('updateLoading', false)
          router.push(`/articles/${res.data.data[0].id}`)
        }
      })
      .catch(err => handleError(commit, err, 'error on adding article'))
  },
  getArticle({ commit }, id) {
    authApi
      .get(`articles/${id}`)
      .then(res => {
        if (res.data.status === 'success') {
          commit('getUserArticle', res.data.data[0])
        }
      })
      .catch(err => handleError(commit, err, 'error on fetching article'))
  },
  getArticles({ commit, dispatch }, params) {
    let url = 'articles'
    if (Object.keys(params).length > 0) {
      url += '?'
      Object.keys(params).map(key => {
        if (key === 'cat_id') {
          dispatch('updateSelectedCategory', +params[key])
        }
        if (key === 'not_read') {
          dispatch('updateReadStatus', params[key])
        }
        if (key === 'tag_id') {
          dispatch('updateSelectedTags', +params[key])
        }
        url += `&${key}=${params[key]}`
      })
    }
    authApi
      .get(url)
      .then(res => {
        if (res.data.status === 'success') {
          if (
            res.data.pagination.pages > 0 &&
            res.data.pagination.page > res.data.pagination.pages
          ) {
            return router.replace(`/articles/page/${res.data.pagination.pages}`)
          }
          commit('getUserArticles', res.data)
        }
      })
      .catch(err => handleError(commit, err, 'error on fetching articles'))
  },
  updateArticle({ commit }, data) {
    authApi
      .patch(`articles/${data.id}`, data.formData)
      .then(res => {
        if (res.data.status === 'success') {
          commit('getUserArticle', res.data.data[0])
        }
      })
      .catch(err => handleError(commit, err, 'error on article update'))
  },
  deleteArticle({ commit, dispatch, state }, id) {
    authApi
      .delete(`articles/${id}`)
      .then(res => {
        if (res.status === 204) {
          dispatch('getArticles', { page: state.pagination.page })
        }
      })
      .catch(err => handleError(commit, err, 'error on article deletion'))
  },
}

export default {
  state,
  getters,
  mutations,
  actions,
}
