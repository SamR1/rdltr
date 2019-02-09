<template>
  <div id="add-article" class="contnr">
    <div class="article-form">
      <div class="title">Add an article</div>
      <hr />
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
      <p v-if="errMessage" class="user-error">{{ errMessage }}</p>
    </div>
  </div>
</template>

<script>
import CategorySelect from '../common/categorySelect'

export default {
  data() {
    return {
      link: '',
    }
  },
  components: {
    AppCategorySelect: CategorySelect,
  },
  computed: {
    errMessage() {
      return this.$store.getters.articleErrorMessage
    },
    selectedCategory() {
      return this.$store.getters.selectedCategory
    },
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
.article-form {
  border: 1px solid #eee;
  box-shadow: 0 2px 3px #ccc;
  margin: 30px auto;
  padding: 20px;
  width: 400px;
}

.add-article-submit {
  margin-top: 0.7em;
}

.title {
  font-weight: bold;
}

@media screen and (max-width: 400px) {
  .article-form {
    width: auto;
  }
}
</style>
