<template>
  <span :class="`badge badge-rdltr${isTag ? '-tag' : ''}`">
    <router-link v-if="isTag" :to="`/?tag_id=${tag_id}`">
      {{ name }}
    </router-link>
    <span v-else>
      {{ name }}
    </span>
  </span>
</template>

<script>
export default {
  props: ['name', 'isTag', 'tag_id'],
}
</script>

<style scoped>
a {
  color: #8c95aa;
  text-decoration: none;
}
.badge-rdltr {
  background-color: #8c95aa;
  box-shadow: 0 1px 2px #ccc;
  color: white;
  margin-bottom: 0.5em;
  margin-top: 1em;
}
.badge-rdltr-tag {
  background-color: #f5f5f7;
  border: 1px solid #8c95aa;
  box-shadow: 0 0.5px 1px #ccc;
  color: #8c95aa;
  margin: 0.5em 0.1em 0.3em 0.1em;
}
</style>
