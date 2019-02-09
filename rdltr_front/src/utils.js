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
