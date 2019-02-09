<template>
  <div class="container">
    <div class="rdltr-box">
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
          <button type="submit" @click.prevent="onSubmit()">Submit</button>
          <router-link
            tag="button"
            to="/settings/categories"
          >Cancel</router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  computed: {
    categoryErrorMessage () {
      return this.$store.getters.categoryErrorMessage
    }
  },
  data () {
    return {
      category: {
        name: '',
        description: ''
      }
    }
  },
  methods: {
    onSubmit () {
      return this.$store.dispatch('addCategory', this.category)
    }
  },
  beforeDestroy () {
    this.$store.commit('updateCategoryErrorMsg', null)
  }
}
</script>

<style scoped>
</style>
