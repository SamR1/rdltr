<template>
  <router-link
    class="clear-filter"
    tag="button"
    to="/"
    v-if="displayClearFilters()"
  >
    &times; clear all filters
  </router-link>
</template>
<script>
export default {
  methods: {
    displayClearFilters() {
      return (
        this.$route.fullPath !== '/' &&
        !this.$route.fullPath.match(/articles\/page\/\d+$/g)
      )
    },
  },
}
</script>

<style scoped>
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
