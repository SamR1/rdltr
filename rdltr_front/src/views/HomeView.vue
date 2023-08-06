<script setup lang="ts">
import ArticlesGrid from '@/components/Article/ArticlesGrid.vue'
import FilterBar from '@/components/Article/FilterBar.vue'
import PaginationComponent from '@/components/Article/Pagination.vue'
</script>

<template>
  <main>
    <div id="home" class="container-fluid">
      <FilterBar />
      <hr />
      <ArticlesGrid />
      <PaginationComponent class="footer" />
    </div>
  </main>
</template>

<style scoped lang="scss">
.add-article {
  border-color: #ccc;
}
</style>
