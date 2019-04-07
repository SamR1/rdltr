<template>
  <div class="tag-input">
    <label v-if="displayLabel">Tags</label>
    <app-multiselect
      placeholder="Search or add a tag"
      v-model="selectedTags"
      :multiple="true"
      :options="userTags"
      :taggable="true"
      @tag="addTag"
    ></app-multiselect>
  </div>
</template>

<script>
import Multiselect from 'vue-multiselect'

export default {
  components: {
    AppMultiselect: Multiselect,
  },
  props: ['displayLabel'],
  computed: {
    selectedTags: {
      get() {
        return this.$store.getters.selectedTags
      },
      set(values) {
        return this.$store.dispatch('updateSelectedTags', values)
      },
    },
    userTags() {
      return this.$store.getters.userTags
        ? this.$store.getters.userTags.map(tag => tag.name)
        : []
    },
  },
  beforeDestroy() {
    return this.$store.dispatch('updateSelectedTags', [])
  },
  methods: {
    addTag(newTag) {
      this.selectedTags.push(newTag)
    },
  },
}
</script>

<style scoped>
.tag-input {
  margin: 0.5em 0;
}
</style>
