<script setup lang="ts">
import { ref, toRefs } from 'vue'
import type { Ref } from 'vue'
import { storeToRefs } from 'pinia'

import { useArticleStore } from '@/stores/articles'
import { useUserStore } from '@/stores/user'

interface Props {
  displayLabel: boolean
  categoryId?: number | null
}
const props = defineProps<Props>()
const { displayLabel, categoryId = null } = toRefs(props)

const articleStore = useArticleStore()
const userStore = useUserStore()
const { userCategories } = storeToRefs(userStore)

const emit = defineEmits(['selected'])

const selectedCategoryId: Ref<number | string> = ref(
  // @ts-ignore
  categoryId.value ? +categoryId.value : ''
)

function updateStore(selectedCategoryId: number | string) {
  articleStore.$patch({
    selectedCategoryId: +selectedCategoryId
  })
  emit('selected', selectedCategoryId)
}
</script>

<template>
  <div id="category-select">
    <label v-if="displayLabel"> Category </label>
    <select
      class="form-control"
      id="categories"
      v-model="selectedCategoryId"
      @change="updateStore(selectedCategoryId)"
    >
      <option value="" v-if="!displayLabel">All categories</option>
      <option
        v-for="category in userCategories"
        :key="category.id"
        :value="category.id"
      >
        {{ category.name }}
      </option>
    </select>
  </div>
</template>
