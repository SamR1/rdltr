<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { onBeforeMount, onUnmounted, ref } from 'vue'
import type { Ref } from 'vue'

import CategorySelect from '@/components/Article/CategorySelect.vue'
import TagMultiSelect from '@/components/Item/TagMultiSelect.vue'
import { useAppStore } from '@/stores/app'
import { useArticleStore } from '@/stores/articles'

const appStore = useAppStore()
const { errorMessage, loading } = storeToRefs(appStore)
const articleStore = useArticleStore()
const { selectedCategoryId, selectedTagsName } = storeToRefs(articleStore)

const link: Ref<string> = ref('')

function onSubmit() {
  const formData = {
    url: link.value,
    category_id: selectedCategoryId.value,
    tags: selectedTagsName.value
  }
  articleStore.addArticle(formData)
}

onBeforeMount(() => articleStore.$patch({ selectedTagsName: [] }))
onUnmounted(() => {
  appStore.setErrorMessage(null)
  articleStore.resetArticleStore()
})
</script>

<template>
  <div class="rdltr-box">
    <div class="title">Add an article</div>
    <hr />
    <p v-if="errorMessage" class="alert alert-danger">
      {{ errorMessage }}
    </p>
    <form @submit.prevent="onSubmit()">
      <div class="input">
        <label for="link">Link</label>
        <input id="link" required v-model="link" />
      </div>
      <CategorySelect :display-label="true" />
      <TagMultiSelect :display-label="true" />
      <div class="submit add-article-submit">
        <button type="submit" :disabled="loading">Submit</button>
      </div>
    </form>
    <div class="text-center" v-if="loading">
      <i class="fa fa-spinner fa-pulse fa-3x fa-fw" />
    </div>
  </div>
</template>

<style scoped lang="scss">
.add-article-submit {
  margin-top: 0.7em;
}

.title {
  font-weight: bold;
}
</style>
