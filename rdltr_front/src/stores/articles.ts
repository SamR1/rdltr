import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Ref } from 'vue'
import type { LocationQuery } from 'vue-router'

import authApi from '@/api/authApi'
import { useUserStore } from '@/stores/user'
import { useAppStore } from '@/stores/app'
import type {
  IAddArticleFormData,
  IArticle,
  IPagination,
  IUpdateArticleFormData
} from '@/types'
import { handleError } from '@/utils'

export const useArticleStore = defineStore('articles', () => {
  const appStore = useAppStore()
  const userStore = useUserStore()

  // state
  const article: Ref<IArticle> = ref(<IArticle>{})
  const articles: Ref<IArticle[]> = ref([])
  const pagination: Ref<IPagination> = ref(<IPagination>{})
  const query: Ref<string> = ref('')
  const selectedCategoryId: Ref<number | null> = ref(null)
  const selectedTagsId: Ref<number[]> = ref([])
  const selectedTagsName: Ref<string[]> = ref([])
  const onlyNotRead: Ref<boolean> = ref(false)
  const onlyFavorites: Ref<boolean> = ref(false)

  // actions
  function addArticle(formData: IAddArticleFormData) {
    appStore.setLoading(true)
    authApi
      .post('articles', formData)
      .then((res) => {
        if (res.data.status === 'success') {
          appStore.setLoading(false)
          // @ts-ignore
          this.router.replace(`/articles/${res.data.data[0].id}`)
        }
      })
      .catch((err) => handleError(err, 'error on adding article'))
  }
  function deleteArticle(articleId: number) {
    authApi
      .delete(`articles/${articleId}`)
      .then((res) => {
        if (res.status === 204) {
          getArticles({ page: pagination.value.page.toString() }, false)
        }
      })
      .catch((err) => handleError(err, 'error on article deletion'))
  }

  function emptyArticle() {
    article.value = <IArticle>{}
  }

  function emptyArticles() {
    articles.value = []
  }

  function getArticle(articleId: number) {
    authApi
      .get(`articles/${articleId}`)
      .then((res) => {
        if (res.data.status === 'success') {
          article.value = res.data.data[0]
          selectedCategoryId.value = article.value.category.id
        }
      })
      .catch((err) => handleError(err, 'error on fetching article'))
  }

  function getArticles(params: {} & LocationQuery, displaySpinner: boolean) {
    if (displaySpinner) {
      appStore.setLoading(true)
    }
    let url = 'articles'
    if (Object.keys(params).length > 0) {
      url += '?'
      Object.keys(params).map((key) => {
        url += `&${key}=${params[key]}`
      })
    }
    selectedCategoryId.value = params.cat_id ? +params.cat_id : null
    selectedTagsId.value = params.tag_id ? [+params.tag_id] : []
    onlyFavorites.value = 'favorites' in params
    onlyNotRead.value = 'not_read' in params
    if (!('q' in params)) {
      query.value = ''
    }
    authApi
      .get(url)
      .then((res) => {
        if (res.data.status === 'success') {
          if (
            res.data.pagination.pages > 0 &&
            res.data.pagination.page > res.data.pagination.pages
          ) {
            // @ts-ignore
            return this.router.replace(
              `/articles/page/${res.data.pagination.pages}`
            )
          }
          articles.value = res.data.data
          pagination.value = res.data.pagination
        }
      })
      .catch((err) => {
        if (err.response?.status === 401) {
          userStore.logout()
        } else {
          handleError(err, 'error on fetching articles')
        }
      })
      .finally(() => appStore.setLoading(false))
  }

  function reloadArticle(articleId: number) {
    appStore.setLoading(true)
    authApi
      .patch(`articles/${articleId}`, { reload: true })
      .then((res) => {
        if (res.data.status === 'success') {
          article.value = res.data.data[0]
          appStore.setLoading(false)
        }
      })
      .catch((err) => handleError(err, 'error on article reload'))
  }

  function updateArticle(
    articleId: number,
    data: IUpdateArticleFormData,
    reloadUserProfile: boolean = false
  ) {
    authApi
      .patch(`articles/${articleId}`, data)
      .then((res) => {
        if (res.data.status === 'success') {
          article.value = res.data.data[0]
          if (reloadUserProfile) {
            userStore.getUserProfile()
          }
        }
      })
      .catch((err) => handleError(err, 'error on article update'))
  }

  function updateQuery(queryValue: string) {
    query.value = queryValue
  }

  function resetArticleStore() {
    article.value = <IArticle>{}
    selectedCategoryId.value = null
    selectedTagsName.value = []
    selectedTagsId.value = []
  }

  return {
    article,
    articles,
    onlyFavorites,
    onlyNotRead,
    pagination,
    query,
    selectedCategoryId,
    selectedTagsId,
    selectedTagsName,
    addArticle,
    deleteArticle,
    emptyArticle,
    emptyArticles,
    getArticle,
    getArticles,
    reloadArticle,
    resetArticleStore,
    updateArticle,
    updateQuery
  }
})
