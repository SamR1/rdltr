<template>
  <div id="article-detail" class="container">
    <router-link to="/" tag="button" class="btn-rdltr">
      Back to home
    </router-link>
    <div v-if="articleErrorMessage">
      <p class="text-center">{{ articleErrorMessage }}</p>
    </div>
    <div v-else>
      <app-category-badge v-if="article.category" :category-name="article.category.name"></app-category-badge>
      <h1>{{ article.title }}</h1>
      <p class="article-link">Link: <a :href="article.url">{{ article.url }}</a></p>
      <app-article-content v-if="article.content" :article-content="article.content"></app-article-content>
    </div>
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
    },
    articleErrorMessage: {
      get () {
        return this.$store.getters.articleErrorMessage
      }
    }
  },
  created () {
    this.$store.dispatch('getArticle', this.$route.params.id)
  },
  beforeDestroy () {
    this.$store.commit('getUserArticle', {})
    this.$store.commit('updateArticlesErrorMsg', null)
  }
}
</script>

<style scoped>
  #article-detail {}

  a {
    color: black;
  }

  .btn-rdltr {
    margin-top: .5em;
  }
</style>
