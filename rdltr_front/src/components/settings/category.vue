<template>
  <div class="contnr">
    <div class="rdltr-box">
      <div v-if="errorMessage && !category.id">
        <p v-if="errorMessage" class="alert alert-danger">
          {{ errorMessage }}
        </p>
        <router-link class="btn-rdltr" tag="button" to="/settings/categories"
          >Back to Categories</router-link
        >
      </div>
      <div v-else>
        <p class="alert alert-danger" v-if="errorMessage">
          {{ errorMessage }}
        </p>
        <form>
          <div class="input">
            <label for="name">Name</label>
            <input id="name" required v-model="category.name" />
          </div>
          <div class="input">
            <label for="description">Description</label>
            <textarea id="description" v-model="category.description">
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
            <router-link tag="button" to="/settings/categories"
              >Cancel</router-link
            >
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      category: {
        id: null,
        name: '',
        description: '',
      },
    }
  },
  computed: {
    errorMessage() {
      return this.$store.getters.errorMessage
    },
    userCategories() {
      return this.$store.getters.userCategories
    },
  },
  beforeDestroy() {
    this.$store.commit('setErrorMessage', null)
  },
  beforeMount() {
    if (this.$route.params.id && this.userCategories) {
      const selectCategory = this.userCategories.filter(
        c => c.id === this.$route.params.id
      )
      if (selectCategory.length > 0) {
        this.category = selectCategory[0]
      } else {
        this.$store.commit('setErrorMessage', 'Category not found!')
      }
    }
  },
  methods: {
    onSubmit() {
      if (this.$route.params.id) {
        return this.$store.dispatch('updateCategory', this.category)
      }
      return this.$store.dispatch('addCategory', this.category)
    },
  },
}
</script>

<style scoped></style>
