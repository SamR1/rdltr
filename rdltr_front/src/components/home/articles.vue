<template>
  <div id="user-articles" class="row">
    <p v-if="articles.length === 0">
      No articles. Add <router-link to="/articles/add">one</router-link>!
    </p>
    <app-article-card
      v-for="article in articles"
      :key="article.id"
      :article="article">
    </app-article-card>
  </div>
</template>

<script>
import ArticleCard from '../articles/articleCard'

export default {
  computed: {
    articles: {
      get () {
        return this.$store.getters.articles
      }
    }
  },
  components: {
    AppArticleCard: ArticleCard
  },
  created () {
    this.$store.dispatch('getArticles')
  }
}
</script>

<style scoped>
  #user-articles{
    margin: .3em;
  }

  a {
    color: black;
  }
</style>
