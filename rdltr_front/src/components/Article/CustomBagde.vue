<script setup lang="ts">
import { toRefs } from 'vue'
import { useRoute } from 'vue-router'

interface Props {
  name: string
  isTag?: boolean
  tagId?: number
}
const props = defineProps<Props>()
const { name, isTag, tagId } = toRefs(props)

const route = useRoute()

function fullPath(tagId: number) {
  if (route.fullPath.match(/\/articles\/\d+/g) || route.fullPath === '/') {
    return `/?tag_id=${tagId}`
  }
  const path = route.fullPath.replace(/articles\/page\/\d+/g, '')
  if (path.includes('tag_id')) {
    return path.replace(/tag_id=\d+/g, `tag_id=${tagId}`)
  }
  return `${path}${path === '/' ? '?' : '&'}tag_id=${tagId}`
}
</script>

<template>
  <span :class="`badge badge-rdltr${isTag ? '-tag' : ''}`">
    <router-link v-if="isTag && tagId" :to="fullPath(tagId)">
      {{ name }}
    </router-link>
    <span v-else>
      {{ name }}
    </span>
  </span>
</template>

<style scoped lang="scss">
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
