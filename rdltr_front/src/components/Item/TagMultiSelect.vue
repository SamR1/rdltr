<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { onBeforeMount, onUnmounted, toRefs, ref } from 'vue'
import type { Ref } from 'vue'
import Multiselect from 'vue-multiselect'

import { useArticleStore } from '@/stores/articles'
import { useUserStore } from '@/stores/user'
import type { ITag } from '@/types'

interface Props {
  displayLabel: boolean
}
const props = defineProps<Props>()
const { displayLabel } = toRefs(props)

const articleStore = useArticleStore()
const { article } = storeToRefs(articleStore)
const userStore = useUserStore()
const { userTags } = storeToRefs(userStore)

const selectedTags: Ref<ITag[]> = ref([])
const options: Ref<ITag[]> = ref([...userTags.value])

function addTag(tagName: string) {
  const newTag: ITag = {
    name: tagName,
    id: 0,
    nb_articles: 0,
    user_id: 0
  }
  options.value.push(newTag)
  selectedTags.value.push(newTag)
  articleStore.$patch({
    selectedTagsName: selectedTags.value.map((t) => t.name)
  })
}
function updateSelectedTag(tags: ITag[]) {
  articleStore.$patch({
    selectedTagsName: tags.map((t) => t.name)
  })
}

onBeforeMount(() => {
  if (article.value && article.value.tags) {
    selectedTags.value = article.value.tags
    articleStore.$patch({
      selectedTagsName: article.value.tags.map((tag: ITag) => tag.name)
    })
  }
})
onUnmounted(() =>
  articleStore.$patch({
    selectedTagsName: []
  })
)
</script>

<template>
  <div class="tag-input">
    <label v-if="displayLabel">Tags</label>
    <Multiselect
      placeholder="Search or add a tag"
      v-model="selectedTags"
      :multiple="true"
      :options="options"
      :taggable="true"
      label="name"
      track-by="name"
      @update:model-value="updateSelectedTag"
      @tag="addTag"
    />
  </div>
</template>

<style scoped lang="scss">
.tag-input {
  margin: 0.5em 0;
}
</style>
