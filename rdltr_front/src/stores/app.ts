import { ref } from 'vue'
import type { Ref } from 'vue'
import { defineStore } from 'pinia'

export const useAppStore = defineStore('app', () => {
  // state
  const errorMessage: Ref<string | null> = ref<string | null>(null)
  const loading: Ref<boolean> = ref<boolean>(false)

  // actions
  function setErrorMessage(message: string | null) {
    errorMessage.value = message
    loading.value = false
  }
  function setLoading(loadingStatus: boolean) {
    loading.value = loadingStatus
    errorMessage.value = null
  }
  return { errorMessage, loading, setErrorMessage, setLoading }
})
