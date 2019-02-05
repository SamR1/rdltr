<template>
  <div>
    <label v-if="displayLabel">
      Category
    </label>
    <select
      class="form-control"
      id="categories"
      v-model="selectedCategory"
    >
      <option
        :key="category.id"
        :value="category.id"
        v-for="category in userCategories"
      >
        {{ category.name }}
      </option>
    </select>
  </div>
</template>

<script>
export default {
  props: ['displayLabel'],
  computed: {
    selectedCategory: {
      get () {
        return this.$store.getters.selectedCategory
      },
      set (value) {
        this.$store.commit('updateCategory', value)
      }
    },
    userCategories () {
      return this.$store.getters.userCategories
    }
  },
  beforeDestroy () {
    this.$store.commit('updateCategory', '')
  }
}
</script>

<style scoped>

</style>
