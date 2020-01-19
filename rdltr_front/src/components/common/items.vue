<template>
  <div class="container container-shadow">
    <div class="row">
      <router-link to="/settings" tag="button" class="btn-rdltr">
        Back to settings
      </router-link>
      <router-link
        class="btn-rdltr"
        tag="button"
        :to="{ name: `add${itemType === 'categories' ? 'Category' : 'Tag'}` }"
      >
        Add a {{ itemType === 'categories' ? 'category' : 'tag' }}
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
    <div v-if="items" class="row items-row">
      <app-items-tables
        :data="items"
        :columns="itemsColumns"
        :filter-key="searchQuery"
        :item-type="itemType"
      >
      </app-items-tables>
    </div>
  </div>
</template>

<script>
import ItemsTable from './itemsTable'

export default {
  components: {
    AppItemsTables: ItemsTable,
  },
  props: ['itemType'],
  data() {
    return {
      displayAdd: false,
      searchQuery: '',
    }
  },
  computed: {
    errorMessage() {
      return this.$store.getters.errorMessage
    },
    itemsColumns() {
      return this.itemType === 'categories'
        ? ['id', 'name', 'description', 'nb_articles']
        : ['id', 'name', 'nb_articles']
    },
    items() {
      return this.itemType === 'categories'
        ? this.$store.getters.userCategories
        : this.$store.getters.userTags
    },
  },
  beforeDestroy() {
    this.$store.dispatch('updateErrorMessage', null)
  },
}
</script>

<style scoped>
.container-shadow {
  border: 1px solid #eee;
  box-shadow: 0 2px 3px #ccc;
  margin-top: 0.5em;
}

.row {
  margin: 1em 0;
}
</style>
