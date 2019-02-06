<template>
  <div class="col-sm-6 col-md-4 col-lg-3">
    <div class="card">
      <div class="card-body">
        <app-category-badge :category-name="article.category.name"></app-category-badge>
        <h5 class="card-title">{{ article.title }}</h5>
        <p class="card-text"></p>
      </div>
      <div class="card-footer">
        <router-link
          :to="{ name: 'articleDetail', params: { id: article.id }}"
          tag="button"
          class="btn-rdltr"
        >
          Read
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import CategoryBadge from '../common/categoryBadge'
export default {
  props: ['article'],
  components: {
    AppCategoryBadge: CategoryBadge
  }
}
</script>

<style scoped>
  .card {
    box-shadow: 0 2px 3px #ccc;
    margin: .5em 0;
  }

  .card-footer {
    background-color: transparent;
    border: none;
  }

</style>
