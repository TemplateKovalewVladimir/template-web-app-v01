<script setup lang="ts">
import { PropType } from 'vue'
import { Column } from './types'
import { Icon } from '@/components/Icon'

const { column } = defineProps({
  column: {
    type: Object as PropType<Column>,
    required: true
  }
})
</script>
<template>
  <div class="flex">
    <slot :column="column">
      <div class="text w-full">{{ column.label }}</div>
      <div><icon :size="12" color="blue" icon="fluent-mdl2:filter-descending" /></div>
    </slot>
  </div>
</template>
