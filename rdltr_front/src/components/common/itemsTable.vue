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
            {{ key | capitalize }}
            <span class="arrow" :class="sortOrders[key] > 0 ? 'asc' : 'dsc'">
            </span>
          </th>
          <th scope="col">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in filteredData" :key="item.id">
          <td v-for="key in columns" :key="key">
            {{ item[key] }}
            <span
              class="badge badge-rdltr badge-rdltr-small"
              v-if="key === 'name' && item.is_default"
            >
              default
            </span>
          </td>
          <td>
            <router-link
              class="link"
              :to="{ name: 'editCategory', params: { id: item.id } }"
            >
              <i class="fa fa-pencil" aria-hidden="true"></i>
            </router-link>
            <i
              aria-hidden="true"
              class="fa fa-trash link"
              v-if="!item.is_default"
              @click="deleteItem(item.id)"
            ></i>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  props: {
    data: Array,
    columns: Array,
    filterKey: String,
  },
  data: function() {
    const sortOrders = {}
    this.columns.forEach(function(key) {
      sortOrders[key] = 1
    })
    return {
      sortKey: '',
      sortOrders: sortOrders,
    }
  },
  computed: {
    filteredData: function() {
      const sortKey = this.sortKey ? this.sortKey : 'id'
      const filterKey = this.filterKey && this.filterKey.toLowerCase()
      const order = this.sortOrders[sortKey] || 1
      let data = this.data
      if (filterKey) {
        data = data.filter(function(row) {
          return Object.keys(row).some(function(key) {
            return (
              String(row[key])
                .toLowerCase()
                .indexOf(filterKey) > -1
            )
          })
        })
      }
      if (sortKey) {
        data = data.slice().sort(function(a, b) {
          a = a[sortKey]
          b = b[sortKey]
          return (a === b ? 0 : a > b ? 1 : -1) * order
        })
      }
      return data
    },
  },
  filters: {
    capitalize: function(str) {
      return str.charAt(0).toUpperCase() + str.slice(1)
    },
  },
  methods: {
    deleteItem(Id) {
      return this.$store.dispatch('deleteCategory', Id)
    },
    sortBy: function(key) {
      this.sortKey = key
      this.sortOrders[key] = this.sortOrders[key] * -1
    },
  },
}
</script>

<style scoped>
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
  font-size: 0.7em;
}
</style>
