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
        <app-tag-multi-select :display-label="true"></app-tag-multi-select>
        <div class="submit add-article-submit">
          <button type="submit" :disabled="loading">Submit</button>
        </div>
      </form>
      <div class="text-center" v-if="loading">
        <i class="fa fa-spinner fa-pulse fa-3x fa-fw"></i>
      </div>
    </div>
  </div>
</template>

<script>
import CategorySelect from '../common/categorySelect'
import TagMultiSelect from '../common/tagMultiSelect'

export default {
  components: {
    AppCategorySelect: CategorySelect,
    AppTagMultiSelect: TagMultiSelect,
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
    loading() {
      return this.$store.getters.loading
    },
    selectedCategory() {
      return this.$store.getters.selectedCategory
    },
    selectedTags() {
      return this.$store.getters.selectedTags
    },
  },
  beforeDestroy() {
    this.$store.commit('setErrorMessage', null)
  },
  mounted() {
    this.$store.commit('setTags', [])
  },
  methods: {
    onSubmit() {
      const formData = {
        url: this.link,
        category_id: this.selectedCategory,
        tags: this.selectedTags,
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
