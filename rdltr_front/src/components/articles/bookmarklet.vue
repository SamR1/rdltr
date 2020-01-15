<template>
  <div id="add-article" class="contnr">
    <div class="rdltr-box">
      <div class="title">Adding shared article</div>
      <hr />
      <p v-if="errorMessage" class="alert alert-danger">
        {{ errorMessage }}
      </p>
      <div class="text-center" v-if="loading">
        <i class="fa fa-spinner fa-pulse fa-3x fa-fw" />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      link: '',
    }
  },
  computed: {
    errorMessage() {
      return this.$store.getters.errorMessage
    },
    isAuthenticated() {
      return this.$store.getters.isAuthenticated
    },
    loading() {
      return this.$store.getters.loading
    },
  },
  beforeDestroy() {
    this.$store.commit('setErrorMessage', null)
  },
  mounted() {
    if (this.isAuthenticated) {
      if (this.$route.query.url) {
        const formData = {
          url: this.$route.query.url,
        }
        return this.$store.dispatch('addArticle', formData)
      } else {
        this.$store.commit('setErrorMessage', 'Error: no URL provided.')
      }
    }
  },
}
</script>

<style scoped />
