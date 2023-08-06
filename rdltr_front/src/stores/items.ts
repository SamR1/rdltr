import { defineStore } from 'pinia'

import authApi from '@/api/authApi'
import { useUserStore } from '@/stores/user'
import type { IItemFormData } from '@/types'
import { handleError } from '@/utils'

export const useItemsStore = defineStore('items', () => {
  const userStore = useUserStore()

  // actions
  async function addItem(formData: IItemFormData) {
    authApi
      .post(formData.type, {
        name: formData.name,
        description: formData.description
      })
      .then((res) => {
        if (res.data.status === 'success') {
          userStore.getUserProfile()
        } else {
          handleError(null)
        }
      })
      .catch((err) => handleError(err, 'error on category creation'))
  }

  async function updateItem(formData: IItemFormData) {
    authApi
      .patch(`${formData.type}/${formData.id}`, {
        name: formData.name,
        description: formData.description
      })
      .then((res) => {
        if (res.data.status === 'success') {
          userStore.getUserProfile()
        } else {
          handleError(null)
        }
      })
      .catch((err) => handleError(err, 'error on category update'))
  }

  async function deleteItem(itemId: number, itemType: string) {
    authApi
      .delete(`${itemType}/${itemId}`)
      .then((res) => {
        if (res.status === 204) {
          userStore.getUserProfile()
        } else {
          handleError(null)
        }
      })
      .catch((err) => handleError(err, 'error on category deletion'))
  }

  return { addItem, deleteItem, updateItem }
})
