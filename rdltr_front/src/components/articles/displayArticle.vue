<template>
  <div id="article-detail" class="container">
    <router-link to="/" tag="button" class="btn-rdltr">
      Back to home
    </router-link>
    <div v-if="articleErrorMessage">
      <p class="text-center">{{ articleErrorMessage }}</p>
    </div>
    <div v-else>
      <div id="category-update" v-if="onCategoryEdition">
        <app-category-select displayLabel="false"></app-category-select>
        <div class="submit">
          <button
            class="btn-rdltr"
            type="submit"
            :disabled="selectedCategory === ''"
            @click="onUpdateCategory"
          >
            Update
          </button>
          <button
            class="btn-rdltr"
            @click="onCategoryEdition=!onCategoryEdition"
          >
            Cancel
          </button>
        </div>
      </div>
      <div v-else>
        <app-category-badge
          v-if="article.category"
          :category-name="article.category.name"
        ></app-category-badge>
        <i
          class="fa fa-pencil link"
          aria-hidden="true"
          @click="updateSelectedCategory"
        ></i>
      </div>
      <h1>{{ article.title }}</h1>
      <p class="article-link">Link:
        <a :href="article.url">
          {{ article.url }}
        </a></p>
      <app-article-content
        v-if="article.content"
        :article-content="article.content"
      ></app-article-content>
      <hr>
      <app-article-comments
        v-if="article.comments"
        :article-comments="article.comments"
      ></app-article-comments>
    </div>
  </div>
</template>

<script>
import ArticleContent from './displayArticleContent'
import ArticleComments from './articleComments'
import CategoryBadge from '../common/categoryBadge'
import CategorySelect from '../common/categorySelect'

export default {
  components: {
    AppCategoryBadge: CategoryBadge,
    AppCategorySelect: CategorySelect,
    AppArticleComments: ArticleComments,
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
    },
    selectedCategory: {
      get () {
        return this.$store.getters.selectedCategory
      }
    }
  },
  methods: {
    onUpdateCategory () {
      this.$store.dispatch('updateArticle', {
        id: this.$route.params.id,
        formData: {
          category_id: this.selectedCategory
        }
      }).then(() => {
        this.onCategoryEdition = false
      })
    },
    updateSelectedCategory () {
      this.$store.commit('updateCategory', this.article.category.id)
      this.onCategoryEdition = !this.onCategoryEdition
    }
  },
  data () {
    return {
      onCategoryEdition: false
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
  #category-update {
    display: inline-flex;
    margin: .7em 0;
  }

  #category-update button {
    margin-left: .5em;
  }

  a {
    color: black;
  }

  .fa {
    font-size: .8em;
  }

</style>
