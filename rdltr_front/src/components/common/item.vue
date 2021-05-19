<template>
  <div class="contnr">
    <div class="rdltr-box">
      <div v-if="errorMessage && !item.id">
        <p v-if="errorMessage" class="alert alert-danger">
          {{ errorMessage }}
        </p>
        <router-link
          class="btn-rdltr"
          tag="button"
          :to="`/settings/${itemType}`"
        >
          Back to {{ itemType }}
        </router-link>
      </div>
      <div v-else>
        <p class="alert alert-danger" v-if="errorMessage">
          {{ errorMessage }}
        </p>
        <form>
          <div class="input">
            <label for="name">{{
              `${itemType === 'categories' ? 'Category' : 'Tag'} name`
            }}</label>
            <input id="name" required v-model="item.name" />
          </div>
          <div class="input" v-if="itemType === 'categories'">
            <label for="description">Description</label>
            <textarea id="description" v-model="item.description" />
          </div>
          <div class="submit">
            <button
              :disabled="item.name === ''"
              class="btn-rdltr"
              type="submit"
              @click.prevent="onSubmit()"
            >
              Submit
            </button>
            <router-link
              class="btn-rdltr"
              tag="button"
              :to="`/settings/${itemType}`"
            >
              Cancel
            </router-link>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { getActionValue } from '@/utils'

export default {
  props: ['itemType'],
  data() {
    return {
      item: {
        id: null,
        name: '',
        description: '',
      },
    }
  },
  computed: {
    errorMessage() {
      return this.$store.getters.errorMessage
    },
    items() {
      return this.itemType === 'categories'
        ? this.$store.getters.userCategories
        : this.$store.getters.userTags
    },
  },
  watch: {
    items: function(newItems) {
      this.getItems(newItems)
    },
  },
  created() {
    this.getItems(this.items)
  },
  beforeDestroy() {
    this.$store.dispatch('updateErrorMessage', null)
  },
  methods: {
    getItems(newItems) {
      if (this.$route.params.id && newItems) {
        const selectItem = newItems.filter(
          item => item.id === +this.$route.params.id
        )
        if (selectItem.length > 0) {
          this.item = selectItem[0]
        } else {
          this.$store.dispatch(
            'updateErrorMessage',
            `${getActionValue(this.itemType, ['singular'])} not found!`
          )
        }
      }
    },
    onSubmit() {
      return this.$store.dispatch(
        `${this.$route.params.id ? 'update' : 'add'}${getActionValue(
          this.itemType,
          ['capitalize', 'singular']
        )}`,
        this.item
      )
    },
  },
}
</script>

<style scoped />
