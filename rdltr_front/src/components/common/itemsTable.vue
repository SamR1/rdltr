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
            {{ key | formatText }}
            <span class="arrow" :class="sortOrders[key] > 0 ? 'asc' : 'dsc'">
            </span>
          </th>
          <th scope="col">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in filteredData" :key="item.id">
          <td v-for="key in columns" :key="key">
            <router-link
              v-if="key === 'name'"
              :to="`/?${itemType === 'categories' ? 'cat' : 'tag'}_id=${
                item.id
              }`"
            >
              {{ item[key] }}
            </router-link>
            <span v-else>
              {{ item[key] }}
            </span>
            <span
              class="badge badge-rdltr-small"
              v-if="key === 'name' && item.is_default"
            >
              default
            </span>
          </td>
          <td>
            <router-link
              class="link"
              :to="{
                name: `edit${target}`,
                params: { id: item.id },
              }"
            >
              <i aria-hidden="true" class="fa fa-pencil" />
            </router-link>
            <i
              aria-hidden="true"
              class="fa fa-trash link"
              v-if="!item.is_default"
              @click="deleteItem(item.id)"
            />
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { getActionValue, capitalize } from '@/utils'

export default {
  props: {
    data: Array,
    columns: Array,
    filterKey: String,
    itemType: String,
  },
  filters: {
    formatText: function (str) {
      return capitalize(str).replace('_', ' ')
    },
  },
  data: function () {
    const sortOrders = {}
    this.columns.forEach(function (key) {
      sortOrders[key] = 1
    })
    return {
      sortKey: '',
      sortOrders: sortOrders,
      target: getActionValue(this.itemType, ['singular', 'capitalize']),
    }
  },
  computed: {
    filteredData: function () {
      const sortKey = this.sortKey ? this.sortKey : 'id'
      const filterKey = this.filterKey && this.filterKey.toLowerCase()
      const order = this.sortOrders[sortKey] || 1
      let data = this.data
      if (filterKey) {
        data = data.filter(function (row) {
          return Object.keys(row).some(function (key) {
            return String(row[key]).toLowerCase().indexOf(filterKey) > -1
          })
        })
      }
      if (sortKey) {
        data = data.slice().sort(function (a, b) {
          a = a[sortKey]
          b = b[sortKey]
          return (a === b ? 0 : a > b ? 1 : -1) * order
        })
      }
      return data
    },
  },
  methods: {
    deleteItem(Id) {
      return this.$store.dispatch(`delete${this.target}`, Id)
    },
    sortBy: function (key) {
      this.sortKey = key
      this.sortOrders[key] = this.sortOrders[key] * -1
    },
  },
}
</script>

<style scoped>
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
  margin: 0;
}
</style>
