<template>
  <div id="article-detail" class="container">
    <app-category-badge v-if="article.category" :category-name="article.category.name"></app-category-badge>
    <h1>{{ article.title }}</h1>
    <p class="article-link">Link: <a :href="article.url">{{ article.url }}</a></p>
    <app-article-content v-if="article.content" :article-content="article.content"></app-article-content>
  </div>
</template>

<script>
import ArticleContent from './displayArticleContent'
import CategoryBadge from '../common/categoryBadge'
export default {
  components: {
    AppCategoryBadge: CategoryBadge,
    AppArticleContent: ArticleContent
  },
  computed: {
    article: {
      get () {
        return this.$store.getters.article
      }
    }
  },
  created () {
    this.$store.dispatch('getArticle', this.$route.params.id)
  },
  beforeDestroy () {
    this.$store.commit('getUserArticle', '')
  }
}
</script>

<style scoped>
  #article-detail {
    margin: 2em;
  }
</style>
