<template>
  <div class="container container-shadow">
    <div class="row">
      <router-link to="/settings" tag="button" class="btn-rdltr">
        Back to settings
      </router-link>
      <router-link class="btn-rdltr" tag="button" :to="{ name: 'addCategory' }">
        Add a category
      </router-link>
    </div>
    <div v-if="errorMessage" class="row">
      <p class="alert alert-danger">
        {{ errorMessage }}
      </p>
    </div>
    <div class="row">
      <div class="input-group">
        <div class="input-group-prepend">
          <span class="input-group-text" id="">Search</span>
        </div>
        <input class="form-control" v-model="searchQuery" />
      </div>
    </div>
    <div v-if="userCategories" class="row items-row">
      <app-items-tables
        :data="userCategories"
        :columns="categoriesColumns"
        :filter-key="searchQuery"
      >
      </app-items-tables>
    </div>
  </div>
</template>

<script>
import ItemsTable from '../common/itemsTable'

export default {
  components: {
    AppItemsTables: ItemsTable,
  },
  data() {
    return {
      categoriesColumns: ['id', 'name', 'description'],
      displayAdd: false,
      searchQuery: '',
    }
  },
  computed: {
    errorMessage() {
      return this.$store.getters.errorMessage
    },
    userCategories() {
      return this.$store.getters.userCategories
    },
  },
  beforeDestroy() {
    this.$store.commit('setErrorMessage', null)
  },
}
</script>

<style scoped>
.btn-rdltr {
  margin-right: 0.5em;
}

.container-shadow {
  border: 1px solid #eee;
  box-shadow: 0 2px 3px #ccc;
  margin-top: 0.5em;
}

.row {
  margin: 1em 0;
}
</style>
