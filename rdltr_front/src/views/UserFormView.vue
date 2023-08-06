<script setup lang="ts">
import { toRefs } from 'vue'
import UserForm from '@/components/User/UserForm.vue'

interface Props {
  actionType: string
}
const props = defineProps<Props>()
const { actionType } = toRefs(props)
</script>

<template>
  <main>
    <UserForm :actionType="actionType" />
  </main>
</template>
