<script setup lang="ts">
import { PropType, computed } from 'vue'
import { Column } from './types'
import { Icon } from '@/components/Icon'

const { column } = defineProps({
  column: {
    type: Object as PropType<Column>,
    required: true
  }
})

const iconName = computed<string | null>(() => {
  if (column.sort === 'ASC') return 'fluent-mdl2/sort-up'
  if (column.sort === 'DESC') return 'fluent-mdl2/sort-down'
  return null
})
</script>
<template>
  <div class="flex">
    <slot :column="column">
      <div class="text w-full" :class="{ 'c-red': column.sort }">{{ column.label }}</div>
      <div v-if="column.sort">
        <icon v-if="iconName" :icon="iconName" :size="12" color="blue" />
      </div>
    </slot>
  </div>
</template>
