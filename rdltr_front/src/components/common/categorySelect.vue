<template>
  <div>
    <label v-if="displayLabel==='true'">
      Category
    </label>
    <select
      class="form-control"
      id="categories"
      v-model="selectedCategory"
      @change="filterArticles"
    >
      <option v-if="!displayLabel" value="">All categories</option>
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
  props: ['displayLabel', 'filter'],
  computed: {
    selectedCategory: {
      get () {
        return this.$store.getters.selectedCategory
      },
      set (value) {
        this.$store.commit('updateCategory', value)
      }
    },
    pagination () {
      return this.$store.getters.pagination
    },
    userCategories () {
      return this.$store.getters.userCategories
    }
  },
  methods: {
    filterArticles () {
      if (this.filter) {
        this.$store.dispatch('getArticles', {
          cat_id: this.selectedCategory,
          page: this.pagination.page
        })
      }
    }
  },
  beforeDestroy () {
    this.$store.commit('updateCategory', '')
  }
}
</script>

<style scoped>

</style>
