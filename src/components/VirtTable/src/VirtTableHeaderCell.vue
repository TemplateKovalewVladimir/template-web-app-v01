<script setup lang="ts">
import { computed, PropType } from 'vue'

import { Icon } from '@/components/Icon'

import { Column } from './types'

const props = defineProps({
  column: {
    type: Object as PropType<Column>,
    required: true
  }
})

const iconName = computed<string | null>(() => {
  const isFilter = props.column.filters.length > 0
  const isASC = props.column.sort === 'ASC'
  const isDESC = props.column.sort === 'DESC'

  if (isFilter && isASC) return 'fluent-mdl2/filter-ascending'
  if (isFilter && isDESC) return 'fluent-mdl2/filter-descending'
  if (isFilter) return 'fluent-mdl2/filter'
  if (isASC) return 'fluent-mdl2/sort-up'
  if (isDESC) return 'fluent-mdl2/sort-down'

  return null
})
</script>
<template>
  <div class="flex">
    <slot :column="column">
      <div class="text w-full" :class="{ 'c-blue': iconName, 'cursor-pointer': column.menu }">{{
        column.label
      }}</div>
      <div>
        <icon v-if="iconName" :icon="iconName" :size="12" color="#60A5FA" />
      </div>
    </slot>
  </div>
</template>
