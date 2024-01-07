<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { useRouter } from 'vue-router'

import { getTargetLocationFromStore } from '@/utils'
import { useArticleStore } from '@/stores/articles'

const articleStore = useArticleStore()
const { pagination } = storeToRefs(articleStore)

const router = useRouter()

function displayFirstPage() {
  return pagination.value.page > 2 && pagination.value.pages > 2
}
function displayLastPage() {
  return pagination.value.pages - 2 >= pagination.value.page
}
function getTargetLink(offset: number) {
  router.push(getTargetLocationFromStore(offset))
}
</script>

<template>
  <div id="pagination" class="row">
    <div class="col-md-2 col-sm text-center">
      <button
        class="btn-rdltr"
        type="submit"
        v-show="displayFirstPage()"
        @click="getTargetLink(1 - pagination.page)"
        title="first page"
      >
        <i class="fa fa-angle-double-left" aria-hidden="true"></i>
      </button>
      <button
        class="btn-rdltr"
        type="submit"
        v-show="pagination.has_prev"
        @click="getTargetLink(-1)"
        title="previous page"
      >
        <i class="fa fa-angle-left" aria-hidden="true"></i>
      </button>
    </div>
    <div class="col-md-8 col-sm text-center page" v-if="pagination.pages > 0">
      page {{ pagination.page }} / {{ pagination.pages }}
    </div>
    <div class="col-md-2 col-sm text-center">
      <button
        class="btn-rdltr"
        type="submit"
        v-show="pagination.has_next"
        @click="getTargetLink(1)"
        title="next page"
      >
        <i class="fa fa-angle-right" aria-hidden="true"></i>
      </button>
      <button
        class="btn-rdltr"
        type="submit"
        v-show="displayLastPage()"
        @click="getTargetLink(pagination.pages - pagination.page)"
        title="last page"
      >
        <i class="fa fa-angle-double-right" aria-hidden="true"></i>
      </button>
    </div>
  </div>
</template>

<style scoped lang="scss">
#pagination {
  align-items: center;
  margin-top: 0.5em;
}

.page {
  font-size: 0.8em;
  font-weight: bold;
}
</style>
