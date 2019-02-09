export const handleError = (commit, err, msg) => {
  if (err.response) {
    return commit('setErrorMessage', err.response.data.message)
  }
  return commit('setErrorMessage', err.message ? err.message : msg)
}
