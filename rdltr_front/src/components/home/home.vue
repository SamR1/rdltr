<template>
  <div id="home" class="container-fluid">
    <div class="row">
      <div class="col">
        <div id="user-categories" class="row">
          <div class="col-md-3">
            <app-category-select></app-category-select>
          </div>
          <div class="col search">
            <div class="input-group">
              <input class="form-control" v-model="query">
              <div class="input-group-btn">
                <button type="submit" class="btn-rdltr">Search</button>
              </div>
            </div>
          </div>
          <div class="col-md-1">
            <router-link
              to="/articles/add"
              tag="button"
              type="submit"
              class="btn-rdltr"
            >
              <i class="fa fa-plus-square" aria-hidden="true"></i>
            </router-link>
          </div>
        </div>
      </div>
    </div>
    <hr>
    <div class="row">
      <app-articles></app-articles>
    </div>
  </div>
</template>

<script>
import Articles from './articles'
import CategorySelect from '../common/categorySelect'

export default {
  data: () => {
    return {
      query: ''
    }
  },
  components: {
    AppArticles: Articles,
    AppCategorySelect: CategorySelect
  }
}
</script>

<style scoped>
  #user-categories{
    align-items: center;
    padding-top: 1em;
    text-align: center;
  }

  .search input {
    margin-right: .5em;
  }

  @media (max-width: 767.98px) {
    .search {
      margin-top: .5em;
      margin-bottom: .5em;
    }
  }
</style>
