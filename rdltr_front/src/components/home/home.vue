<template>
  <div id="home" class="container-fluid">
    <div class="row">
      <div class="col">
        <div id="user-categories" class="row">
          <div class="col-md-3">
            <select
              class="form-control"
              id="categories"
              v-model="selectedCategory"
            >
              <option
                :key="category.id"
                v-for="category in userCategories"
              >
                {{ category.name }}
              </option>
            </select>
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
            <button type="submit" class="btn-rdltr">
              <i class="fa fa-plus-square" aria-hidden="true"></i>
            </button>
          </div>
        </div>
      </div>
    </div>
    <hr>
    <div class="row">
      <div class="col">
        <app-articles></app-articles>
      </div>
    </div>
  </div>
</template>

<script>
import Articles from './articles'

export default {
  data: () => {
    return {
      query: '',
      selectedCategory: ''
    }
  },
  components: {
    AppArticles: Articles
  },
  computed: {
    userCategories () {
      return this.$store.getters.userCategories
    }
  }
}
</script>

<style scoped>
  #home {
    color: #4e4e4e;
  }

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

  .btn-rdltr {
    background-color: #f5f5f7;
    border: 1px solid #8c95aa;
    color: #8c95aa;
    height: calc(2.25rem + 2px);
    padding: 0.5em 0.8em;
    font: inherit;
    cursor: pointer;
  }

  .btn-rdltr:hover{
    background-color: #8c95aa;
    color: white;
  }
</style>
