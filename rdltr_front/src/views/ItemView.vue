<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { computed, toRefs } from 'vue'
import type { ComputedRef } from 'vue'

import Item from '@/components/Item/Item.vue'
import { useUserStore } from '@/stores/user'
import type { ICategory, ITag, TItemType } from '@/types'

interface Props {
  itemType: TItemType
}
const props = defineProps<Props>()
const { itemType } = toRefs(props)

const userStore = useUserStore()
const { authUser } = storeToRefs(userStore)

const items: ComputedRef<ICategory[] | ITag[]> = computed(() =>
  authUser.value ? authUser.value[itemType.value] : []
)
</script>

<template>
  <div class="contnr">
    <Item :item-type="itemType" :items="items" />
  </div>
</template>
