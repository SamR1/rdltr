<script setup lang="ts">
import { onMounted, toRefs, watch } from 'vue'

interface Props {
  articleContent: string
}
const props = defineProps<Props>()
const { articleContent } = toRefs(props)

function displayContent() {
  const element = document.getElementById('article-content')
  if (element) {
    element.innerHTML = articleContent.value
  }
}

watch(
  () => articleContent,
  async () => {
    displayContent()
  }
)

onMounted(() => displayContent())
</script>

<template>
  <div class="article-content" id="article-content"></div>
</template>

<style scoped lang="scss">
.article-content {
  padding: 1em;
}
</style>
