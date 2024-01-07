<script setup lang="ts">
import { ref, toRefs } from 'vue'
import type { Ref } from 'vue'

import CustomBadge from '@/components/Article/CustomBagde.vue'
import ConfirmationModal from '@/components/Article/DeleteConfirmationModal.vue'
import { useArticleStore } from '@/stores/articles'
import type { IArticle } from '@/types'

interface Props {
  article: IArticle
}
const props = defineProps<Props>()
const { article } = toRefs(props)

const articleStore = useArticleStore()

const showModal: Ref<boolean> = ref(false)

function onDeleteArticle() {
  articleStore.deleteArticle(article.value.id)
}
</script>

<template>
  <div class="col-sm-6 col-md-4 col-lg-3">
    <ConfirmationModal
      v-if="showModal"
      :title="article.title"
      @delete="onDeleteArticle"
      @close="showModal = false"
    />
    <div class="card" :class="`status${article.read ? '-read' : ''}`">
      <div class="card-body">
        <button
          aria-label="Close"
          class="close"
          title="delete article"
          type="button"
          @click="showModal = true"
        >
          <span aria-hidden="true">&times;</span>
        </button>
        <CustomBadge :name="article.category.name" />
        <h5 class="card-title">
          {{ article.title }} <i v-if="article.favorite" class="fa fa-star" />
        </h5>
        <CustomBadge
          v-for="tag in article.tags"
          :tagId="tag.id"
          :isTag="true"
          :key="tag.id"
          :name="tag.name"
        />
        <p class="card-text" />
      </div>
      <div class="card-footer">
        <button
          class="btn-rdltr"
          @click="
            $router.push({ name: 'ArticleDetail', params: { id: article.id } })
          "
        >
          Read
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.card {
  box-shadow: 0 2px 3px #ccc;
  margin: 0.5em 0;
}

.card-footer {
  background-color: transparent;
  border: none;
}

.status-read {
  opacity: 0.5;
}
</style>
