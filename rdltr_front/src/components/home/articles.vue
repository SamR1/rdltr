<template>
  <div id="user-articles">
    <div v-if="articleErrorMessage">
      <p class="text-center">{{ articleErrorMessage }}</p>
    </div>
    <div v-else>
      <div class="row articles-msg" v-if="pagination.total > 0">
        {{ pagination.total }}
        {{ `article${pagination.total !== 1 ? 's' : ''}` }}
      </div>
      <div class="row">
        <p v-if="articles.length === 0" class="text-center articles-msg">
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
import ArticleCard from '../articles/articleCard'
import Pagination from './pagination'

export default {
  computed: {
    articleErrorMessage: {
      get() {
        return this.$store.getters.articleErrorMessage
      },
    },
    articles: {
      get() {
        return this.$store.getters.articles
      },
    },
    pagination: {
      get() {
        return this.$store.getters.pagination
      },
    },
  },
  components: {
    AppArticleCard: ArticleCard,
    AppPagination: Pagination,
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

a {
  color: black;
}

.articles-msg {
  margin-left: 1em;
}
</style>
