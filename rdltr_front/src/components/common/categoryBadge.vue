<template>
  <span class="badge badge-rdltr">
    {{ categoryName }}
  </span>
</template>

<script>
export default {
  props: ['categoryName'],
  computed: {
    categories () {
      return this.$store.getters.user.categories
    }
  }
}
</script>

<style scoped>
  .badge-rdltr {
    background-color: #8c95aa;
    color: white;
    margin-bottom: .5em;
  }
</style>
