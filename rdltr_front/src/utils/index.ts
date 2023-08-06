import type { AxiosError } from 'axios'
import { storeToRefs } from 'pinia'
import type { LocationQueryRaw, RouteLocationRaw } from 'vue-router'

import { useAppStore } from '@/stores/app'
import { useArticleStore } from '@/stores/articles'
import type { IApiErrorMessage } from '@/types'

export const getApiUrl = (): string => {
  return import.meta.env.PROD ? '/api' : 'http://localhost:5000/api'
}

export const handleError = (
  error: AxiosError | null,
  msg = 'Error. Please try again or contact the administrator.'
) => {
  if (error && error.message === 'canceled') {
    return
  }
  const errorInfo: IApiErrorMessage | null =
    error?.response && error.response.data ? error.response.data : null

  const appStore = useAppStore()
  const { errorMessage } = storeToRefs(appStore)

  errorMessage.value = !error
    ? msg
    : error.response
    ? errorInfo?.message
      ? errorInfo.message
      : msg
    : error.message
    ? error.message
    : msg
}

export const capitalize = (str: string): string =>
  str.charAt(0).toUpperCase() + str.slice(1)

export const getActionValue = (
  itemType: string,
  transformation: string[]
): string => {
  let result = itemType
  if (transformation.includes('singular')) {
    result = itemType === 'categories' ? 'category' : 'tag'
  }
  if (transformation.includes('capitalize')) {
    result = capitalize(result)
  }
  return result
}

export const getTargetLocationFromStore = (
  pageOffset = 0
): RouteLocationRaw => {
  const articleStore = useArticleStore()
  const {
    selectedTagsId,
    onlyNotRead,
    onlyFavorites,
    query,
    pagination,
    selectedCategoryId
  } = storeToRefs(articleStore)
  const location: RouteLocationRaw =
    pagination.value.page > 1 || pageOffset !== 0
      ? {
          name: 'Articles',
          params: { page: pagination.value.page + pageOffset }
        }
      : { name: 'Home' }
  const articlesQuery = <LocationQueryRaw>{}
  if (selectedCategoryId.value) {
    articlesQuery.cat_id = selectedCategoryId.value
  }
  if (query.value) {
    articlesQuery.q = query.value
  }
  if (onlyFavorites.value) {
    articlesQuery.favorites = 'true'
  }
  if (onlyNotRead.value) {
    articlesQuery.not_read = 'true'
  }
  if (selectedTagsId.value.length > 0) {
    articlesQuery.tag_id = selectedTagsId.value[0]
  }
  location.query = articlesQuery
  return location
}

export const displayWithBrowserTimezone = (date: string) => {
  const browserTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone
  const articleDate = new Date(date)
  return articleDate.toLocaleString('en-GB', {
    weekday: 'long',
    month: 'long',
    day: 'numeric',
    year: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
    second: '2-digit',
    hour12: false,
    timeZone: browserTimezone
  })
}
