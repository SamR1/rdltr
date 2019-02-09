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
export default {
  props: ['displayLabel', 'filter'],
  computed: {
    selectedCategory: {
      get() {
        return this.$store.getters.selectedCategory
      },
      set(value) {
        this.$store.commit('setCategory', value)
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
    this.$store.commit('setCategory', '')
  },
  methods: {
    filterArticles() {
      if (this.filter) {
        this.$store.dispatch('getArticles', {
          cat_id: this.selectedCategory,
          page: this.pagination.page,
        })
      }
    },
  },
}
</script>

<style scoped></style>
