<template>
  <div id="user-articles">
    <div class="row">
      <p v-if="articles.length === 0">
        No articles. Add <router-link to="/articles/add">one</router-link>!
      </p>
      <app-article-card
        v-for="article in articles"
        :key="article.id"
        :article="article">
      </app-article-card>
    </div>
    <app-pagination></app-pagination>
  </div>
</template>

<script>
import ArticleCard from '../articles/articleCard'
import Pagination from './pagination'

export default {
  computed: {
    articles: {
      get () {
        return this.$store.getters.articles
      }
    }
  },
  components: {
    AppArticleCard: ArticleCard,
    AppPagination: Pagination
  },
  watch: {
    '$route' (to, from) {
      this.$store.dispatch('getArticles', to.params)
    }
  },
  created () {
    this.$store.dispatch('getArticles', this.$route.params)
  }
}
</script>

<style scoped>
  #user-articles{
    margin: 1em;
    width: 100%;
  }

  a {
    color: black;
  }
</style>
