<template>
  <div class="container" id="article-detail">
    <router-link class="btn-rdltr" tag="button" to="/">
      Back to home
    </router-link>
    <p v-if="errorMessage" class="alert alert-danger">
      {{ errorMessage }}
    </p>
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
            @click="onCategoryEdition = !onCategoryEdition"
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
          aria-hidden="true"
          class="fa fa-pencil link"
          @click="updateSelectedCategory"
        ></i>
      </div>
      <h1>{{ article.title }}</h1>
      <p class="article-link">
        Link:
        <a :href="article.url">
          {{ article.url }}
        </a>
      </p>
      <app-article-content
        v-if="article.content"
        :article-content="article.content"
      ></app-article-content>
      <hr />
      <app-article-comments
        v-if="article"
        :article-comments="article.comments"
      ></app-article-comments>
    </div>
  </div>
</template>

<script>
import ArticleContent from './articleContentDisplay'
import ArticleComments from './articleComments'
import CategoryBadge from '../common/categoryBadge'
import CategorySelect from '../common/categorySelect'

export default {
  components: {
    AppCategoryBadge: CategoryBadge,
    AppCategorySelect: CategorySelect,
    AppArticleComments: ArticleComments,
    AppArticleContent: ArticleContent,
  },
  data() {
    return {
      onCategoryEdition: false,
    }
  },
  computed: {
    article: {
      get() {
        return this.$store.getters.article
      },
    },
    errorMessage: {
      get() {
        return this.$store.getters.errorMessage
      },
    },
    selectedCategory: {
      get() {
        return this.$store.getters.selectedCategory
      },
    },
  },
  created() {
    this.$store.dispatch('getArticle', this.$route.params.id)
  },
  beforeDestroy() {
    this.$store.commit('getUserArticle', {})
    this.$store.commit('setErrorMessage', null)
  },
  methods: {
    onUpdateCategory() {
      this.$store
        .dispatch('updateArticle', {
          id: this.$route.params.id,
          formData: {
            category_id: this.selectedCategory,
          },
        })
        .then(() => {
          this.onCategoryEdition = false
        })
    },
    updateSelectedCategory() {
      this.$store.commit('setCategory', this.article.category.id)
      this.onCategoryEdition = !this.onCategoryEdition
    },
  },
}
</script>

<style scoped>
#category-update {
  display: inline-flex;
  margin: 0.7em 0;
}

#category-update button {
  margin-left: 0.5em;
}

.fa {
  font-size: 0.8em;
}

a {
  color: black;
}
</style>
