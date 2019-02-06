<template>
  <div class="article-content" id="article-content"></div>
</template>

<script>
export default {
  props: ['articleContent'],
  methods: {
    displayContent () {
      const x = document.getElementById('article-content')
      x.innerHTML = this.articleContent
    }
  },
  mounted () {
    this.displayContent()
  }
}
</script>

<style scoped>
  .article-content{
    padding: 1em;
  }
</style>
