<script setup lang="ts">
import { computed, ref, toRefs } from 'vue'
import type { ComputedRef, Ref } from 'vue'

import { useItemsStore } from '@/stores/items'
import type {
  ICategory,
  TCategoryColumns,
  TItemQueryColumns,
  ISortOrder,
  ITag,
  TTagColumns
} from '@/types'
import { capitalize, getActionValue } from '@/utils'

interface Props {
  items: ICategory[] | ITag[]
  columns: TTagColumns[] | TCategoryColumns[]
  searchQuery: string
  itemType: string
}
const props = defineProps<Props>()
const { items, columns, searchQuery, itemType } = toRefs(props)

const itemStore = useItemsStore()

const sortKey: Ref<TCategoryColumns | TTagColumns> = ref('id')
const sortOrders: Ref<ISortOrder> = ref({
  id: 1,
  type: 1,
  name: 1,
  description: 1,
  nb_articles: 1
})

const target: ComputedRef<string> = computed(() =>
  getActionValue(itemType.value, ['singular', 'capitalize'])
)
const filteredData: ComputedRef<ICategory[] | ITag[]> = computed(() =>
  filterData(items.value, searchQuery.value)
)

function formatText(str: string): string {
  return capitalize(str).replace('_', ' ')
}
function matchesQuery(
  item: ICategory | ITag,
  key: TItemQueryColumns,
  query: string
): boolean {
  return (
    // @ts-ignore
    key in item && item[key].toLowerCase().indexOf(query.toLowerCase()) > -1
  )
}
function filterData(
  dataToFilter: ICategory[] | ITag[],
  query: string
): ICategory[] | ITag[] {
  let filtered: ICategory[] | ITag[] = [...dataToFilter]
  if (query) {
    filtered = filtered.filter(
      (item) =>
        matchesQuery(item, 'name', query) ||
        matchesQuery(item, 'description', query)
    )
  }

  const order: number = sortOrders.value[sortKey.value] || 1
  filtered = filtered.slice().sort(function (a, b) {
    if (sortKey.value in a && sortKey.value in b) {
      // @ts-ignore
      a = a[sortKey.value]
      // @ts-ignore
      b = b[sortKey.value]
    }
    return (a === b ? 0 : a > b ? 1 : -1) * order
  })
  return filtered
}
function deleteItem(id: number) {
  itemStore.deleteItem(id, itemType.value)
}
function sortBy(key: TCategoryColumns | TTagColumns) {
  sortKey.value = key
  sortOrders.value[key] = sortOrders.value[key] * -1
}
</script>

<template>
  <div class="table-responsive">
    <table class="table">
      <thead>
        <tr>
          <th
            scope="col"
            v-for="key in columns"
            :class="{ active: sortKey === key }"
            :key="key"
            @click="sortBy(key)"
          >
            <button class="icon-transparent">
              {{ formatText(key) }}
              <span class="arrow" :class="sortOrders[key] > 0 ? 'asc' : 'dsc'">
              </span>
            </button>
          </th>
          <th scope="col">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in filteredData" :key="item.id">
          <td>
            <span>
              {{ item.id }}
            </span>
          </td>
          <td>
            <router-link
              :to="`/?${itemType === 'categories' ? 'cat' : 'tag'}_id=${
                item.id
              }`"
            >
              {{ item.name }}
            </router-link>
            <span
              class="badge badge-rdltr-small"
              v-if="'is_default' in item && item.is_default"
            >
              default
            </span>
          </td>
          <td v-if="'description' in item">
            <span>
              {{ item.description }}
            </span>
          </td>
          <td>
            <span>
              {{ item.nb_articles }}
            </span>
          </td>
          <td>
            <router-link
              class="link"
              :to="{
                name: `Edit${target}`,
                params: { id: item.id }
              }"
              title="edit item"
            >
              <i aria-hidden="true" class="fa fa-pencil" />
            </router-link>
            <button
              class="icon-transparent"
              v-if="!('is_default' in item && item.is_default)"
              @click="deleteItem(item.id)"
              title="delete item"
            >
              <i aria-hidden="true" class="fa fa-trash link" />
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped lang="scss">
a {
  color: #8c95aa;
  text-decoration: none;
}

.arrow {
  display: inline-block;
  vertical-align: middle;
  width: 0;
  height: 0;
  margin-left: 5px;
  opacity: 0.66;
}

.arrow.asc {
  border-left: 4px solid transparent;
  border-right: 4px solid transparent;
  border-bottom: 4px solid #4e4e4e;
}

.arrow.dsc {
  border-left: 4px solid transparent;
  border-right: 4px solid transparent;
  border-top: 4px solid #4e4e4e;
}

.badge-rdltr-small {
  background-color: #8c95aa;
  box-shadow: 0 1px 2px #ccc;
  color: white;
  font-size: 0.7em;
  margin-left: 5px;
}
</style>
