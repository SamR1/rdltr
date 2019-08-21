<template>
  <div class="container" id="article-detail">
    <conf-modal
      v-if="showModal"
      :onDeleteArticle="onDeleteArticle"
      @close="showModal = false"
    ></conf-modal>
    <button class="btn-rdltr" type="submit" @click="$router.go(-1)">
      Back
    </button>
    <p v-if="errorMessage" class="alert alert-danger">
      {{ errorMessage }}
    </p>
    <div v-if="article.title">
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
        <router-link
          style="cursor: pointer"
          tag="span"
          v-if="article.category"
          :to="`/?cat_id=${article.category.id}`"
        >
          <app-badge :name="article.category.name"></app-badge>
        </router-link>
        <i
          aria-hidden="true"
          class="fa fa-pencil link"
          title="edit category"
          @click="updateSelectedCategory"
        ></i>
        <i
          aria-hidden="true"
          :class="`fa fa-eye${article.read ? '-slash' : ''}`"
          :title="`mark as ${article.read ? 'not ' : ''}read`"
          @click="updateReadStatus"
        ></i>
        <i
          aria-hidden="true"
          title="reload article"
          :class="`fa fa-refresh${loading ? ' fa-spin' : ''}`"
          @click="onReloadArticle"
        ></i>
        <i
          aria-hidden="true"
          title="delete article"
          :class="`fa fa-trash${loading ? ' fa-disabled' : ''}`"
          @click="showModal = true"
        ></i>
      </div>
      <h1>{{ article.title }}</h1>
      <div id="tag-update" v-if="onTagEdition">
        <app-tag-multi-select></app-tag-multi-select>
        <div class="submit">
          <button class="btn-rdltr" type="submit" @click="onUpdateTags">
            Update
          </button>
          <button class="btn-rdltr" @click="onTagEdition = !onTagEdition">
            Cancel
          </button>
        </div>
      </div>
      <div v-else>
        <app-badge
          v-for="tag in article.tags"
          :display-label="false"
          :tag_id="tag.id"
          :is-tag="true"
          :key="tag.id"
          :name="tag.name"
        ></app-badge>
        <span
          class="no-tags"
          v-show="article.tags && article.tags.length === 0"
        >
          no tags
        </span>
        <i
          aria-hidden="true"
          class="fa fa-pencil link"
          title="edit tags"
          @click="updateSelectedTags"
        ></i>
      </div>
      <p class="article-link">
        Link:
        <a :href="article.url" target="_blank " rel="noopener noreferrer">
          {{ article.url }}
        </a>
      </p>
      <app-article-content
        v-if="article.html_content"
        :article-content="article.html_content"
      ></app-article-content>
      <button class="btn-rdltr" type="submit" @click="$router.go(-1)">
        Back
      </button>
      <button class="btn-rdltr" type="submit" @click.prevent="updateReadStatus">
        {{ `Mark as ${article.read ? 'not ' : ''}read` }}
      </button>
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
import CategorySelect from '../common/categorySelect'
import ConfModal from '../common/deleteConfirmationModal'
import CustomBadge from '../common/customBagde'
import TagMultiSelect from '../common/tagMultiSelect'

export default {
  components: {
    AppBadge: CustomBadge,
    AppCategorySelect: CategorySelect,
    AppArticleComments: ArticleComments,
    AppArticleContent: ArticleContent,
    AppTagMultiSelect: TagMultiSelect,
    ConfModal: ConfModal,
  },
  data() {
    return {
      onCategoryEdition: false,
      onTagEdition: false,
      showModal: false,
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
    loading: {
      get() {
        return this.$store.getters.loading
      },
    },
    selectedCategory: {
      get() {
        return this.$store.getters.selectedCategory
      },
    },
    selectedTags: {
      get() {
        return this.$store.getters.selectedTags
      },
    },
  },
  created() {
    if (this.$store.getters.isAuthenticated) {
      return this.$store.dispatch('getArticle', this.$route.params.id)
    }
  },
  beforeDestroy() {
    this.$store.commit('getUserArticle', {})
    this.$store.commit('setErrorMessage', null)
  },
  methods: {
    onDeleteArticle() {
      if (!this.loading) {
        this.$store
          .dispatch('deleteArticle', this.article.id)
          .then(() => this.$router.push('/'))
      }
    },
    onReloadArticle() {
      const data = {
        id: this.article.id,
        formData: { reload: true },
      }
      return this.$store.dispatch('reloadArticle', data)
    },
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
    onUpdateTags() {
      this.$store
        .dispatch('updateArticle', {
          id: this.$route.params.id,
          formData: {
            tags: this.selectedTags,
          },
        })
        .then(() => {
          this.onTagEdition = false
        })
    },
    updateReadStatus() {
      const data = {
        id: this.article.id,
        formData: { update_read_status: !this.article.read },
      }
      return this.$store.dispatch('updateArticle', data)
    },
    updateSelectedCategory() {
      return this.$store
        .dispatch('updateSelectedCategory', this.article.category.id)
        .then(() => (this.onCategoryEdition = !this.onCategoryEdition))
    },
    updateSelectedTags() {
      const tags = this.article.tags.map(tag => tag.name)
      return this.$store
        .dispatch('updateSelectedTags', tags)
        .then(() => (this.onTagEdition = !this.onTagEdition))
    },
  },
}
</script>

<style scoped>
#category-update {
  display: inline-flex;
  margin: 0.7em 0;
}

.article-link {
  margin-top: 1em;
}

.fa {
  color: #8c95aa;
}

.fa-disabled {
  opacity: 0.5;
}

.fa-pencil {
  font-size: 0.8em;
}

.no-tags {
  font-size: 0.9em;
  font-style: italic;
}

a {
  color: black;
}
</style>
