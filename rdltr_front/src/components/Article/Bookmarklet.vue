<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { onMounted } from 'vue'
import { useRoute } from 'vue-router'

import { useAppStore } from '@/stores/app'
import { useArticleStore } from '@/stores/articles'
import { useUserStore } from '@/stores/user'

const route = useRoute()

const appStore = useAppStore()
const { errorMessage, loading } = storeToRefs(appStore)
const userStore = useUserStore()
const { isAuthenticated } = storeToRefs(userStore)
const articleStore = useArticleStore()

onMounted(() => {
  if (isAuthenticated.value) {
    if (route.query.url) {
      articleStore.addArticle({
        url: `${route.query.url}`
      })
    } else {
      appStore.setErrorMessage('Error: no URL provided.')
    }
  }
})
</script>

<template>
  <div id="add-article" class="contnr">
    <div class="rdltr-box">
      <div class="title">Adding shared article</div>
      <hr />
      <p v-if="errorMessage" class="alert alert-danger">
        {{ errorMessage }}
      </p>
      <div class="text-center" v-if="loading">
        <i class="fa fa-spinner fa-pulse fa-3x fa-fw" />
      </div>
    </div>
  </div>
</template>

<style scoped />
