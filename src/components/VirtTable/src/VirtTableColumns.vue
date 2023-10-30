<script setup lang="ts">
import { PropType } from 'vue'
import { Column } from './types'

const { columns } = defineProps({
  columns: {
    type: Array as PropType<Column[]>,
    required: true
  }
})
</script>
<template>
  <div
    v-for="column in columns"
    :key="column.prop"
    class="cell"
    :style="column.width !== 0 ? `flex: 0 0 auto; width: ${column.width}px` : ''"
  >
    <slot :column="column" />
  </div>
</template>
