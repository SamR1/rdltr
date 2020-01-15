<template>
  <div id="home" class="container-fluid">
    <div class="row">
      <div class="col">
        <div id="user-categories" class="row">
          <div class="col-md-3">
            <app-category-select filter="true" />
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
          <div class="col-md-2 form-check read-status">
            <input
              class="form-check-input"
              id="readStatus"
              type="checkbox"
              v-model="onlyNotRead"
              @change="onSearch"
            />
            <label class="form-check-label" for="readStatus">
              only not read
            </label>
          </div>
          <div class="col-md-2 form-check favorite">
            <input
              class="form-check-input"
              id="favorites"
              type="checkbox"
              v-model="onlyFavorites"
              @change="onSearch"
            />
            <label class="form-check-label" for="favorites">
              only favorites
            </label>
          </div>
        </div>
      </div>
    </div>
    <hr />
    <div class="row">
      <app-articles />
    </div>
  </div>
</template>

<script>
import Articles from '../articles/articlesList'
import CategorySelect from '../common/categorySelect'
import { getTargetLocationFromStore } from '../../utils'

export default {
  components: {
    AppArticles: Articles,
    AppCategorySelect: CategorySelect,
  },
  computed: {
    onlyFavorites: {
      get() {
        return this.$store.getters.onlyFavorites
      },
      set(value) {
        this.$store.dispatch('updateFavorites', value)
      },
    },
    onlyNotRead: {
      get() {
        return this.$store.getters.onlyNotRead
      },
      set(value) {
        this.$store.dispatch('updateReadStatus', value)
      },
    },
    query: {
      get() {
        return this.$store.getters.query
      },
      set(value) {
        this.$store.dispatch('updateQuery', value)
      },
    },
  },
  methods: {
    onSearch() {
      this.$router.push(getTargetLocationFromStore(this.$store.getters))
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
}

@media (max-width: 767.98px) {
  .search {
    margin-bottom: 0.5em;
    margin-top: 0.5em;
  }
}
</style>
