export const handleError = (commit, err, msg) => {
  if (err.response) {
    return commit('setErrorMessage', err.response.data.message)
  }
  return commit('setErrorMessage', err.message ? err.message : msg)
}

export const capitalize = str => str.charAt(0).toUpperCase() + str.slice(1)

export const getActionValue = (itemType, transformation) => {
  let result = itemType
  if (transformation.includes('singular')) {
    result = itemType === 'categories' ? 'category' : 'tag'
  }
  if (transformation.includes('capitalize')) {
    result = capitalize(result)
  }
  return result
}

export const getTargetLocationFromStore = (store, pageOffset = 0) => {
  const location =
    store.page || pageOffset !== 0
      ? {
          name: 'articlesPage',
          params: { page: store.pagination.page + pageOffset },
        }
      : { name: 'home' }
  const query = {}
  if (store.selectedCategory) {
    query.cat_id = store.selectedCategory
  }
  if (store.query) {
    query.q = store.query
  }
  if (store.onlyNotRead) {
    query.not_read = store.onlyNotRead
  }
  location.query = query
  return location
}
