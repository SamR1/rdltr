<script setup lang="ts">
import { toRefs } from 'vue'

import ItemsList from '@/components/Item/ItemsList.vue'
import type { TItemType } from '@/types'

interface Props {
  itemType: TItemType
}
const props = defineProps<Props>()
const { itemType } = toRefs(props)
</script>

<template>
  <main>
    <ItemsList :itemType="itemType" />
  </main>
</template>
