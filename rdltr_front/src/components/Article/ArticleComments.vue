<script setup lang="ts">
import { onBeforeMount, ref, toRefs } from 'vue'
import type { Ref } from 'vue'
import { useRoute } from 'vue-router'

import { useArticleStore } from '@/stores/articles'

interface Props {
  articleComments: string | null
}
const props = defineProps<Props>()
const { articleComments } = toRefs(props)

const articleStore = useArticleStore()

const route = useRoute()

const comments: Ref<string> = ref('')
const onCommentsEdition: Ref<boolean> = ref(false)

function onSubmit() {
  articleStore.updateArticle(
    +route.params.id,
    {
      comments: comments.value ? comments.value : null
    },
    true
  )
  onCommentsEdition.value = false
}

onBeforeMount(() => (comments.value = articleComments.value || ''))
</script>

<template>
  <form>
    <div class="input">
      <label for="description">Comments</label>
      <textarea
        id="description"
        v-if="onCommentsEdition"
        v-model="comments"
        :disabled="!onCommentsEdition"
      >
      </textarea>
      <p id="comments" v-else>{{ comments ? comments : 'No comments yet' }}</p>
    </div>
    <div class="submit" v-if="onCommentsEdition">
      <button class="btn-rdltr" type="submit" @click.prevent="onSubmit">
        Submit
      </button>
      <button
        class="btn-rdltr"
        type="submit"
        @click.prevent="onCommentsEdition = !onCommentsEdition"
      >
        Cancel
      </button>
    </div>
    <div v-else>
      <button
        class="btn-rdltr"
        type="submit"
        @click.prevent="onCommentsEdition = !onCommentsEdition"
      >
        Edit comments
      </button>
    </div>
  </form>
</template>

<style scoped lang="scss">
#comments {
  font-style: italic;
  margin: 0.5em;
  white-space: pre;
}
</style>
