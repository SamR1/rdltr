<template>
  <div id="pagination" class="row">
    <div class="col-md-2 col-sm text-center">
      <button
        class="btn-rdltr"
        type="submit"
        v-show="displayFirstPage()"
        @click="getTargetLink(1 - pagination.page)"
      >
        <i class="fa fa-angle-double-left " aria-hidden="true"></i>
      </button>
      <button
        class="btn-rdltr"
        type="submit"
        v-show="pagination.has_prev"
        @click="getTargetLink(-1)"
      >
        <i class="fa fa-angle-left" aria-hidden="true"></i>
      </button>
    </div>
    <div class="col-md-8 col-sm text-center page" v-if="pagination.pages > 0">
      page {{ pagination.page }} / {{ pagination.pages }}
    </div>
    <div class="col-md-2 col-sm text-center">
      <button
        class="btn-rdltr"
        type="submit"
        v-show="pagination.has_next"
        @click="getTargetLink(1)"
      >
        <i class="fa fa-angle-right" aria-hidden="true"></i>
      </button>
      <button
        class="btn-rdltr"
        type="submit"
        v-show="displayLastPage()"
        @click="getTargetLink(pagination.pages - pagination.page)"
      >
        <i class="fa fa-angle-double-right" aria-hidden="true"></i>
      </button>
    </div>
  </div>
</template>

<script>
import { getTargetLocationFromStore } from '@/utils'

export default {
  computed: {
    pagination() {
      return this.$store.getters.pagination
    },
  },
  methods: {
    displayFirstPage() {
      return this.pagination.page > 2 && this.pagination.pages > 2
    },
    displayLastPage() {
      return this.pagination.pages - 2 >= this.pagination.page
    },
    getTargetLink(offset) {
      this.$router.push(getTargetLocationFromStore(this.$store.getters, offset))
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
