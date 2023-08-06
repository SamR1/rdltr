<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { computed, onBeforeMount, watch } from 'vue'
import type { ComputedRef } from 'vue'
import { useRoute } from 'vue-router'

import ArticleCard from '@/components/Article/ArticleCard.vue'
import ClearFilter from '@/components/Article/ClearFilter.vue'
import CustomBadge from '@/components/Article/CustomBagde.vue'
import { useAppStore } from '@/stores/app'
import { useArticleStore } from '@/stores/articles'
import { useUserStore } from '@/stores/user'
import type { ITag } from '@/types'

const appStore = useAppStore()
const { errorMessage, loading } = storeToRefs(appStore)
const articleStore = useArticleStore()
const { articles, pagination } = storeToRefs(articleStore)
const userStore = useUserStore()
const { userTags } = storeToRefs(userStore)

const route = useRoute()

const tag: ComputedRef<ITag | null> = computed(() => getTag())

function getTag() {
  if (route.query.tag_id && userTags.value) {
    const tagId = +route.query.tag_id
    const filteredTags = userTags.value.filter((tag) => tag.id === tagId)
    if (filteredTags.length > 0) {
      return filteredTags[0]
    }
  }
  return null
}
function getArticles(displaySpinner = false) {
  const params = Object.assign({}, route.query)
  articleStore.getArticles(params, displaySpinner)
}

watch(
  () => route.query,
  async () => {
    getArticles()
  }
)

onBeforeMount(() => getArticles(true))
</script>

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
            <CustomBadge :tagId="tag.id" :isTag="true" :name="tag.name" />
          </div>
          <clearFilter />
        </div>
        <div class="row">
          <p class="text-center articles-msg" v-if="articles.length === 0">
            No articles. Add
            <router-link to="/articles/add">one</router-link>
            ! <clearFilter />
          </p>
          <ArticleCard
            v-for="article in articles"
            :key="article.id"
            :article="article"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
#user-articles {
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
</style>
