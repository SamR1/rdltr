<template>
  <div id="user-articles">
    <p v-if="errorMessage" class="alert alert-danger">
      {{ errorMessage }}
    </p>
    <div v-else>
      <div class="text-center" v-if="loading">
        <i class="fa fa-spinner fa-pulse fa-3x fa-fw"></i>
      </div>
      <div v-else>
        <div class="row articles-msg" v-if="pagination.total > 0">
          <div>
            {{ pagination.total }}
            {{ `article${pagination.total !== 1 ? 's' : ''}` }}
          </div>
          <div v-if="tag" class="display-tag">
            <app-badge :tag_id="tag.id" :is-tag="true" :name="tag.name" />
          </div>
          <clear-filter></clear-filter>
        </div>
        <div class="row">
          <p class="text-center articles-msg" v-if="articles.length === 0">
            No articles. Add
            <router-link to="/articles/add">one</router-link>
            ! <clear-filter></clear-filter>
          </p>
          <app-article-card
            v-for="article in articles"
            :key="article.id"
            :article="article"
          >
          </app-article-card>
        </div>
      </div>
    </div>
    <app-pagination class="footer" />
  </div>
</template>

<script>
import ArticleCard from './articleCard'
import ClearFilter from './clearFilter'
import CustomBadge from '../common/customBagde'
import Pagination from '../home/pagination'

export default {
  components: {
    AppArticleCard: ArticleCard,
    AppBadge: CustomBadge,
    AppPagination: Pagination,
    ClearFilter: ClearFilter,
  },
  computed: {
    articles() {
      return this.$store.getters.articles
    },
    errorMessage() {
      return this.$store.getters.errorMessage
    },
    loading() {
      return this.$store.getters.loading
    },
    pagination() {
      return this.$store.getters.pagination
    },
    userTags() {
      return this.$store.getters.userTags
    },
    tag: function() {
      if ('tag_id' in this.$route.query && this.userTags) {
        return this.$store.getters.user.tags.filter(
          tag => tag.id === +this.$route.query['tag_id']
        )[0]
      }
      return null
    },
  },
  watch: {
    $route(to) {
      this.$store.dispatch(
        'getArticles',
        Object.assign({}, to.params, to.query)
      )
    },
  },
  created: function() {
    if (this.$store.getters.isAuthenticated) {
      return this.$store.dispatch(
        'getArticles',
        Object.assign({}, this.$route.params, this.$route.query, {
          displaySpinner: true,
        })
      )
    }
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
  align-items: center;
}

.display-tag {
  margin-left: 0.5em;
  margin-top: -4px;
}

.footer {
  bottom: 9px;
  height: 50px;
  margin: -0.5em -1em;
  position: absolute;
  width: 100%;
}

a {
  color: black;
}
</style>
