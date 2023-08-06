<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { computed, onBeforeMount, onBeforeUnmount, ref } from 'vue'
import type { Ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import ArticleComments from '@/components/Article/ArticleComments.vue'
import ArticleContentDisplay from '@/components/Article/ArticleContentDisplay.vue'
import CategorySelect from '@/components/Article/CategorySelect.vue'
import CustomBadge from '@/components/Article/CustomBagde.vue'
import ConfirmationModal from '@/components/Article/DeleteConfirmationModal.vue'
import TagMultiSelect from '@/components/Item/TagMultiSelect.vue'
import { useArticleStore } from '@/stores/articles'
import { useAppStore } from '@/stores/app'
import { displayWithBrowserTimezone } from '@/utils'

const route = useRoute()
const router = useRouter()

const appStore = useAppStore()
const { errorMessage, loading } = storeToRefs(appStore)
const articleStore = useArticleStore()
const { article, selectedCategoryId, selectedTagsName } =
  storeToRefs(articleStore)

const onCategoryEdition: Ref<boolean> = ref(false)
const onTagEdition: Ref<boolean> = ref(false)
const showModal: Ref<boolean> = ref(false)

const articleDate = computed(() =>
  displayWithBrowserTimezone(article.value.date_added)
)

function onDeleteArticle() {
  if (!loading.value) {
    articleStore.deleteArticle(article.value.id)
    router.push('/')
  }
}
function goBack() {
  return window.history.length > 1 ? router.go(-1) : router.push('/')
}
function onReloadArticle() {
  articleStore.reloadArticle(article.value.id)
}
function onUpdateCategory() {
  if (selectedCategoryId.value !== null) {
    articleStore.updateArticle(+route.params.id, {
      category_id: +selectedCategoryId.value
    })
  }
  onCategoryEdition.value = false
}
function onUpdateTags() {
  articleStore.updateArticle(
    +route.params.id,
    {
      tags: selectedTagsName.value
    },
    true
  )
  onTagEdition.value = false
}
function updateFavorite() {
  articleStore.updateArticle(article.value.id, {
    update_favorite: !article.value.favorite
  })
}
function updateReadStatus() {
  articleStore.updateArticle(article.value.id, {
    update_read_status: !article.value.read
  })
}
function updateSelectedCategory(categoryId: number) {
  articleStore.updateArticle(
    article.value.id,
    { category_id: categoryId },
    true
  )
  onCategoryEdition.value = !onCategoryEdition.value
}
function updateSelectedTags() {
  const tags = article.value.tags.map((tag) => tag.name)
  articleStore.$patch({
    selectedTagsName: tags
  })
  onTagEdition.value = !onTagEdition.value
}

onBeforeMount(() => {
  articleStore.getArticle(+route.params.id)
})
onBeforeUnmount(() => {
  articleStore.resetArticleStore()
})
</script>

<template>
  <div class="container" id="article-detail">
    <ConfirmationModal
      v-if="showModal"
      @delete="onDeleteArticle"
      @close="showModal = false"
    />
    <button class="btn-rdltr" type="submit" @click="goBack">Back</button>
    <p v-if="errorMessage" class="alert alert-danger">
      {{ errorMessage }}
    </p>
    <div v-if="article.title">
      <div id="category-update" v-if="onCategoryEdition">
        <CategorySelect
          :displayLabel="false"
          :categoryId="article.category.id"
          @selected="updateSelectedCategory"
        />
        <div class="submit">
          <button
            class="btn-rdltr"
            type="submit"
            :disabled="!selectedCategoryId"
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
          v-if="article.category"
          :to="`/?cat_id=${article.category.id}`"
        >
          <CustomBadge :name="article.category.name" />
        </router-link>
        <i
          aria-hidden="true"
          class="fa fa-pencil link"
          title="edit category"
          @click="onCategoryEdition = !onCategoryEdition"
        />
        <i
          aria-hidden="true"
          :class="`fa fa-eye${article.read ? '-slash' : ''}`"
          :title="`mark as ${article.read ? 'not ' : ''}read`"
          @click="updateReadStatus"
        />
        <i
          aria-hidden="true"
          :class="`fa fa-star${article.favorite ? '' : '-o'}`"
          :title="`${article.favorite ? 'un' : ''} favorite article`"
          @click="updateFavorite"
        />
        <i
          aria-hidden="true"
          title="reload article"
          :class="`fa fa-refresh${loading ? ' fa-spin' : ''}`"
          @click="onReloadArticle"
        />
        <i
          aria-hidden="true"
          title="delete article"
          :class="`fa fa-trash${loading ? ' fa-disabled' : ''}`"
          @click="showModal = true"
        />
      </div>
      <h1>{{ article.title }}</h1>
      <div id="tag-update" v-if="onTagEdition">
        <TagMultiSelect :display-label="false" />
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
        <CustomBadge
          v-for="tag in article.tags"
          :display-label="false"
          :tag_id="tag.id"
          :is-tag="true"
          :key="tag.id"
          :name="tag.name"
        />
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
        />
      </div>
      <p class="article-data">
        <i class="fa fa-calendar-plus-o" aria-hidden="true"></i>
        {{ articleDate }}
        <br />
        <i class="fa fa-link" aria-hidden="true"></i>
        <a :href="article.url" target="_blank " rel="noopener noreferrer">
          {{ article.url }}
        </a>
      </p>
      <ArticleContentDisplay
        v-if="article.html_content"
        :article-content="article.html_content"
      />
      <button class="btn-rdltr" type="submit" @click="$router.go(-1)">
        Back
      </button>
      <button class="btn-rdltr" type="submit" @click.prevent="updateReadStatus">
        {{ `Mark as ${article.read ? 'not ' : ''}read` }}
      </button>
      <hr />
      <ArticleComments :article-comments="article.comments" />
    </div>
  </div>
</template>

<style scoped lang="scss">
#category-update {
  display: inline-flex;
  margin: 0.7em 0;
  .submit {
    padding-left: 10px;
  }
}

.article-data {
  font-size: 0.9em;
  font-style: italic;
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
