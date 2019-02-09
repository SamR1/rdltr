<template>
  <div id="user-articles">
    <div v-if="!errorMessage">
      <div class="row articles-msg" v-if="pagination.total > 0">
        {{ pagination.total }}
        {{ `article${pagination.total !== 1 ? 's' : ''}` }}
      </div>
      <div class="row">
        <p class="text-center articles-msg" v-if="articles.length === 0">
          No articles. Add
          <router-link to="/articles/add">one</router-link>
          !
        </p>
        <app-article-card
          v-for="article in articles"
          :key="article.id"
          :article="article"
        >
        </app-article-card>
      </div>
    </div>
    <app-pagination></app-pagination>
  </div>
</template>

<script>
import ArticleCard from './articleCard'
import Pagination from '../home/pagination'

export default {
  components: {
    AppArticleCard: ArticleCard,
    AppPagination: Pagination,
  },
  computed: {
    articles() {
      return this.$store.getters.articles
    },
    errorMessage() {
      return this.$store.getters.errorMessage
    },
    pagination() {
      return this.$store.getters.pagination
    },
  },
  watch: {
    $route(to, from) {
      this.$store.dispatch('getArticles', to.params)
    },
  },
  created() {
    this.$store.dispatch('getArticles', this.$route.params)
  },
}
</script>

<style scoped>
#user-articles {
  margin: 0.5em 1em;
  width: 100%;
}

.articles-msg {
  margin-left: 1em;
}

a {
  color: black;
}
</style>
