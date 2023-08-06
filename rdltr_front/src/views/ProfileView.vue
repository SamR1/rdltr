<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { toRefs } from 'vue'

import Profile from '@/components/User/Profile.vue'
import { useUserStore } from '@/stores/user'

interface Props {
  actionType: string
}
const props = defineProps<Props>()
const { actionType } = toRefs(props)

const userStore = useUserStore()
const { authUser } = storeToRefs(userStore)
</script>

<template>
  <main>
    <div id="actionType" class="contnr" v-if="authUser">
      <Profile :actionType="actionType"></Profile>
    </div>
  </main>
</template>
