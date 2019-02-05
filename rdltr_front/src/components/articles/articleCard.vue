<template>
  <div class="card">
    <div class="card-body">
      <span class="badge badge-rdltr">
        {{ categories.filter(category => category.id === article.category_id)[0].name }}
      </span>
      <h5 class="card-title">{{ article.title }}</h5>
      <p class="card-text"></p>
    </div>
    <div class="card-footer">
      <router-link to="#" tag="button" class="btn-rdltr">Read</router-link>
    </div>
  </div>
</template>

<script>
export default {
  props: ['article'],
  computed: {
    categories () {
      return this.$store.getters.user.categories
    }
  }
}
</script>

<style scoped>
  .card {
    box-shadow: 0 2px 3px #ccc;
    margin: .5em;
    width: 18rem;
  }

  .badge-rdltr {
    background-color: #8c95aa;
    color: white;
    margin-bottom: .5em;
  }

  .card-footer {
    background-color: transparent;
    border: none;
  }

</style>
