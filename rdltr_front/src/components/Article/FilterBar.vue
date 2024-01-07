<script setup lang="ts">
import { ref } from 'vue'
import type { Ref } from 'vue'
import { useRouter } from 'vue-router'

import CategorySelect from '@/components/Article/CategorySelect.vue'
import { useArticleStore } from '@/stores/articles'
import { getTargetLocationFromStore } from '@/utils'

const articleStore = useArticleStore()

const router = useRouter()

const query: Ref<string> = ref('')
const onlyNotRead: Ref<boolean> = ref(false)
const onlyFavorites: Ref<boolean> = ref(false)

function onSearch() {
  articleStore.$patch({
    onlyFavorites: onlyFavorites.value,
    onlyNotRead: onlyNotRead.value,
    query: query.value
  })
  router.push(getTargetLocationFromStore())
}
</script>

<template>
  <div class="row">
    <div class="col">
      <div id="user-categories" class="row">
        <div class="col-md-3">
          <CategorySelect
            :filter="true"
            :displayLabel="false"
            @selected="onSearch"
          />
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
</template>

<style scoped>
#user-categories {
  align-items: center;
  padding-top: 1em;
  text-align: center;
}
.search input {
  margin-right: 0.5em;
}

.input-group-text {
  background-color: #f5f5f7;
  border-radius: 0;
}

@media (max-width: 768px) {
  .search {
    margin-bottom: 0.5em;
    margin-top: 0.5em;
  }
}
</style>
