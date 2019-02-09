<template>
  <div class="container">
    <div class="rdltr-box">
      <div v-if="categoryErrorMessage && !category.id">
        <p
          v-if="categoryErrorMessage"
          class="alert alert-danger"
        >
          {{ categoryErrorMessage }}
        </p>
        <router-link
          class="btn-rdltr"
          tag="button"
          to="/settings/categories"
        >Back to Categories</router-link>
      </div>
      <div v-else>
        <p
          v-if="categoryErrorMessage"
          class="alert alert-danger"
        >
          {{ categoryErrorMessage }}
        </p>
        <form>
          <div class="input">
            <label for="name">Name</label>
            <input
              id="name"
              required
              v-model="category.name">
          </div>
          <div class="input">
            <label for="description">Description</label>
            <textarea
              id="description"
              v-model="category.description">
            </textarea>
          </div>
          <div class="submit">
            <button
              :disabled="category.name === ''"
              type="submit"
              @click.prevent="onSubmit()"
            >
              Submit
            </button>
            <router-link
              tag="button"
              to="/settings/categories"
            >Cancel</router-link>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      category: {
        id: null,
        name: '',
        description: ''
      }
    }
  },
  computed: {
    userCategories () {
      return this.$store.getters.userCategories
    },
    categoryErrorMessage () {
      return this.$store.getters.categoryErrorMessage
    }
  },
  methods: {
    onSubmit () {
      if (this.$route.params.id) {
        return this.$store.dispatch('updateCategory', this.category)
      }
      return this.$store.dispatch('addCategory', this.category)
    }
  },
  beforeDestroy () {
    this.$store.commit('updateCategoryErrorMsg', null)
  },
  beforeMount () {
    if (this.$route.params.id && this.userCategories) {
      const selectCategory = this.userCategories.filter(c => c.id === this.$route.params.id)
      if (selectCategory.length > 0) {
        this.category = selectCategory[0]
      } else {
        this.$store.commit('updateCategoryErrorMsg', 'Category not found!')
      }
    }
  }
}
</script>

<style scoped>
</style>
