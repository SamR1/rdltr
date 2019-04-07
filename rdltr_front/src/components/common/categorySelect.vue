<template>
  <div>
    <label v-if="displayLabel === 'true'">
      Category
    </label>
    <select
      class="form-control"
      id="categories"
      v-model="selectedCategory"
      @change="filterArticles"
    >
      <option value="" v-if="!displayLabel">All categories</option>
      <option
        v-for="category in userCategories"
        :key="category.id"
        :value="category.id"
      >
        {{ category.name }}
      </option>
    </select>
  </div>
</template>

<script>
import { getTargetLocationFromStore } from '../../utils'

export default {
  props: ['displayLabel', 'filter'],
  computed: {
    selectedCategory: {
      get() {
        return this.$store.getters.selectedCategory
      },
      set(value) {
        return this.$store.dispatch('updateSelectedCategory', value)
      },
    },
    pagination() {
      return this.$store.getters.pagination
    },
    userCategories() {
      return this.$store.getters.userCategories
    },
  },
  beforeDestroy() {
    return this.$store.dispatch('updateSelectedCategory', '')
  },
  methods: {
    filterArticles() {
      if (this.filter) {
        this.$store.commit('setTags', [])
        return this.$router.push(
          getTargetLocationFromStore(this.$store.getters)
        )
      }
    },
  },
}
</script>

<style scoped></style>
