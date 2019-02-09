<template>
  <div id="add-article" class="contnr">
    <div class="rdltr-box">
      <div class="title">Add an article</div>
      <hr />
      <p v-if="errorMessage" class="alert alert-danger">
        {{ errorMessage }}
      </p>
      <form @submit.prevent="onSubmit()">
        <div class="input">
          <label for="link">Link</label>
          <input id="link" required v-model="link" />
        </div>
        <app-category-select display-label="true"></app-category-select>
        <div class="submit add-article-submit">
          <button type="submit">Submit</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import CategorySelect from '../common/categorySelect'

export default {
  components: {
    AppCategorySelect: CategorySelect,
  },
  data() {
    return {
      link: '',
    }
  },
  computed: {
    errorMessage() {
      return this.$store.getters.errorMessage
    },
    selectedCategory() {
      return this.$store.getters.selectedCategory
    },
  },
  beforeDestroy() {
    this.$store.commit('setErrorMessage', null)
  },
  methods: {
    onSubmit() {
      const formData = {
        url: this.link,
        category_id: this.selectedCategory,
      }
      return this.$store.dispatch('addArticle', formData)
    },
  },
}
</script>

<style scoped>
.add-article-submit {
  margin-top: 0.7em;
}

.title {
  font-weight: bold;
}
</style>
