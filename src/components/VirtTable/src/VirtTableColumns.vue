<script setup lang="ts">
import { PropType, computed } from 'vue'
import { Column } from './types'

const { columns } = defineProps({
  columns: {
    type: Array as PropType<Column[]>,
    required: true
  }
})

const emit = defineEmits<{
  (e: 'contextmenu', event: MouseEvent, column: Column): void
}>()

const computedColumns = computed(() => {
  return columns.filter((v) => v.visible)
})
</script>
<template>
  <div
    v-for="column in computedColumns"
    :key="column.prop"
    class="cell"
    :style="column.width !== 0 ? `flex: 0 0 auto; width: ${column.width}px` : ''"
    @contextmenu="emit('contextmenu', $event, column)"
  >
    <slot :column="column" />
  </div>
</template>
