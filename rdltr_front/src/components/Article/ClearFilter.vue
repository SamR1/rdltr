<script setup lang="ts">
import { useRoute } from 'vue-router'

const route = useRoute()

function displayClearFilters() {
  return (
    route.fullPath !== '/' && !route.fullPath.match(/articles\/page\/\d+$/g)
  )
}
</script>

<template>
  <button
    v-if="displayClearFilters()"
    class="clear-filter"
    @click="$router.push('/')"
  >
    &times; clear all filters
  </button>
</template>

<style scoped lang="scss">
.clear-filter {
  background-color: #8c95aa;
  border: 1px solid #8c95aa;
  color: white;
  font-size: 0.9em;
  margin: 0 0.5em 0.5em 1em;
  padding: 0.1em 0.4em 0 0.3em;
}
.clear-filter:hover {
  background-color: #f5f5f7;
  color: #8c95aa;
}
</style>
