<script setup lang="ts">
import { computed, ref, toRefs } from 'vue'
import type { ComputedRef, Ref } from 'vue'
import { storeToRefs } from 'pinia'

import ItemsTable from '@/components/Item/ItemsTable.vue'
import { useAppStore } from '@/stores/app'
import { useUserStore } from '@/stores/user'
import type {
  ICategory,
  TCategoryColumns,
  TItemType,
  ITag,
  TTagColumns
} from '@/types'

interface Props {
  itemType: TItemType
}
const props = defineProps<Props>()
const { itemType } = toRefs(props)

const appStore = useAppStore()
const { errorMessage } = storeToRefs(appStore)
const userStore = useUserStore()
const { authUser } = storeToRefs(userStore)

const searchQuery: Ref<string> = ref('')

const itemsColumns: ComputedRef<TTagColumns[] | TCategoryColumns[]> = computed(
  () =>
    itemType.value === 'categories'
      ? ['id', 'name', 'description', 'nb_articles']
      : ['id', 'name', 'nb_articles']
)
const items: ComputedRef<ICategory[] | ITag[]> = computed(() =>
  authUser.value ? authUser.value[itemType.value] : []
)
</script>

<template>
  <div class="container container-shadow">
    <div class="row">
      <button class="btn-rdltr" @click="$router.push('/settings')">
        Back to settings
      </button>
      <button
        class="btn-rdltr"
        @click="
          $router.push({
            name: `Add${itemType === 'categories' ? 'Category' : 'Tag'}`
          })
        "
      >
        Add a {{ itemType === 'categories' ? 'category' : 'tag' }}
      </button>
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
      <ItemsTable
        :items="items"
        :columns="itemsColumns"
        :searchQuery="searchQuery"
        :item-type="itemType"
      >
      </ItemsTable>
    </div>
  </div>
</template>

<style scoped lang="scss">
.container-shadow {
  border: 1px solid #eee;
  box-shadow: 0 2px 3px #ccc;
  margin-top: 0.5em;
}

.row {
  margin: 1em 0;
}
</style>
