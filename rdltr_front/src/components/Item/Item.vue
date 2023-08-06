<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { onBeforeMount, reactive, toRefs } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { useAppStore } from '@/stores/app'
import { useItemsStore } from '@/stores/items'
import type { ICategory, IItemFormData, ITag } from '@/types'
import { getActionValue } from '@/utils'

interface Props {
  itemType: string
  items: ICategory[] | ITag[]
}
const props = defineProps<Props>()
const { itemType, items } = toRefs(props)

const itemStore = useItemsStore()
const appStore = useAppStore()
const { errorMessage } = storeToRefs(appStore)

const route = useRoute()
const router = useRouter()

const formData: IItemFormData = reactive({
  id: null,
  type: itemType.value,
  name: '',
  description: ''
})

function getItem() {
  if (route.params.id && items.value) {
    const itemId = +route.params.id
    const selectItems: ICategory[] | ITag[] = items.value.filter(
      (i) => i.id === itemId
    )
    if (selectItems.length > 0) {
      const item = selectItems[0]
      formData.id = item.id
      formData.name = item.name
      formData.description =
        // @ts-ignore
        'description' in item.description && item.description
          ? // @ts-ignore
            item.description
          : ''
    } else {
      appStore.setErrorMessage(
        `${getActionValue(itemType.value, ['singular'])} not found!`
      )
    }
  }
}
function onSubmit() {
  if (route.params.id) {
    itemStore.updateItem(formData)
  } else {
    itemStore.addItem(formData)
  }
  router.push(`/settings/${formData.type}`)
}

onBeforeMount(() => getItem())
</script>

<template>
  <div class="rdltr-box">
    <p class="alert alert-danger" v-if="errorMessage">
      {{ errorMessage }}
    </p>
    <form>
      <div class="input">
        <label for="name">{{
          `${itemType === 'categories' ? 'Category' : 'Tag'} name`
        }}</label>
        <input id="name" required v-model="formData.name" />
      </div>
      <div class="input" v-if="itemType === 'categories'">
        <label for="description">Description</label>
        <textarea id="description" v-model="formData.description" />
      </div>
      <div class="submit">
        <button
          :disabled="formData.name === ''"
          class="btn-rdltr"
          type="submit"
          @click.prevent="onSubmit()"
        >
          Submit
        </button>
        <button
          class="btn-rdltr"
          type="submit"
          @click.prevent="$router.push(`/settings/${itemType}`)"
        >
          Cancel
        </button>
      </div>
    </form>
  </div>
</template>

<style scoped lang="scss" />
