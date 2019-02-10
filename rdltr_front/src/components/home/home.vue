<template>
  <div id="home" class="container-fluid">
    <div class="row">
      <div class="col">
        <div id="user-categories" class="row">
          <div class="col-md-3">
            <app-category-select filter="true"></app-category-select>
          </div>
          <div class="col search">
            <div class="input-group">
              <div class="input-group-prepend">
                <span class="input-group-text" id="">Search</span>
              </div>
              <input
                class="form-control"
                placeholder="enter keywords"
                v-model="query"
                @input="onSearch"
              />
            </div>
          </div>
          <div class="col-md-1">
            <router-link
              class="btn-rdltr add-article"
              to="/articles/add"
              tag="button"
              title="add article"
              type="submit"
            >
              <i class="fa fa-plus-square" aria-hidden="true"></i>
            </router-link>
          </div>
        </div>
      </div>
    </div>
    <hr />
    <div class="row">
      <app-articles></app-articles>
    </div>
  </div>
</template>

<script>
import Articles from '../articles/articlesList'
import CategorySelect from '../common/categorySelect'

export default {
  components: {
    AppArticles: Articles,
    AppCategorySelect: CategorySelect,
  },
  computed: {
    query: {
      get() {
        return this.$store.getters.query
      },
      set(value) {
        this.$store.commit('updateQuery', value)
      },
    },
  },
  methods: {
    onSearch() {
      return this.$store.dispatch('getArticles', { query: this.query })
    },
  },
}
</script>

<style scoped>
#user-categories {
  align-items: center;
  padding-top: 1em;
  text-align: center;
}

.add-article {
  border-color: #ccc;
}

.search input {
  margin-right: 0.5em;
}

.input-group-text {
  background-color: #f5f5f7;
  border-radius: 0;
  margin-left: 1em;
}

@media (max-width: 767.98px) {
  .search {
    margin-bottom: 0.5em;
    margin-top: 0.5em;
  }
}
</style>
