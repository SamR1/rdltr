<template>
  <div id="pagination" class="row">
    <div class="col-1 text-center">
      <router-link
        v-show="pagination.has_prev"
        :to="{ name: 'articlesPage', params: { page: pagination.page - 1 } }"
        tag="button"
        type="submit"
        class="btn-rdltr"
      >
        <i class="fa fa-chevron-left" aria-hidden="true"></i>
      </router-link>
    </div>
    <div class="col-10 text-center page" v-if="pagination.pages > 0">
      page {{ pagination.page }} / {{ pagination.pages }}
    </div>
    <div class="col-1 text-center">
      <router-link
        v-show="pagination.has_next"
        :to="{ name: 'articlesPage', params: { page: pagination.page + 1 } }"
        tag="button"
        type="submit"
        class="btn-rdltr"
      >
        <i class="fa fa-chevron-right" aria-hidden="true"></i>
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  computed: {
    pagination: {
      get() {
        return this.$store.getters.pagination
      },
    },
  },
}
</script>

<style scoped>
#pagination {
  align-items: center;
  margin-top: 0.5em;
}

.page {
  font-size: 0.8em;
  font-weight: bold;
}
</style>
