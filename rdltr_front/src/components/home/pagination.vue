<template>
  <div id="pagination" class="row">
    <div class="col-1 text-center">
      <button
        class="btn-rdltr"
        type="submit"
        v-show="pagination.has_prev"
        @click="getTargetLink(-1)"
      >
        <i class="fa fa-chevron-left" aria-hidden="true" />
      </button>
    </div>
    <div class="col-10 text-center page" v-if="pagination.pages > 0">
      page {{ pagination.page }} / {{ pagination.pages }}
    </div>
    <div class="col-1 text-center">
      <button
        class="btn-rdltr"
        type="submit"
        v-show="pagination.has_next"
        @click="getTargetLink(1)"
      >
        <i class="fa fa-chevron-right" aria-hidden="true" />
      </button>
    </div>
  </div>
</template>

<script>
import { getTargetLocationFromStore } from '../../utils'

export default {
  computed: {
    pagination() {
      return this.$store.getters.pagination
    },
  },
  methods: {
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
