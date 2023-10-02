<script setup lang="ts">
import { useVirtualList, useInfiniteScroll } from '@vueuse/core'
import { useDesign } from '@/hooks/web/useDesign'
import { PropType } from 'vue'

import { Column } from './types'

const props = defineProps({
  data: {
    type: Array as PropType<Record<string, any>[]>,
    required: true
  },
  columns: {
    type: Array as PropType<Column[]>,
    required: true
  },
  onLoadMore: {
    type: Function,
    required: true
  },

  height: {
    type: String,
    default: '300px'
  }
})

const { getPrefixCls } = useDesign()
const prefixCls = getPrefixCls('virt-table')

const { list, containerProps, wrapperProps } = useVirtualList(props.data, {
  itemHeight: 28 + 3 * 2
  // overscan: 5
})

useInfiniteScroll(
  containerProps.ref,
  () => {
    props.onLoadMore()
  },
  { distance: 10 }
)
</script>

<template>
  <div v-bind="containerProps" :class="`${prefixCls}-table`" :style="`height: ${props.height}`">
    <div v-bind="wrapperProps">
      <div class="header">
        <!-- Header columns -->
        <div
          v-for="column in columns"
          :key="column.prop"
          class="cell"
          :style="column.width !== 0 ? `flex: 0 0 auto; width: ${column.width}px` : ''"
        >
          <slot name="header" :column="column">{{ column.label }}</slot>
        </div>
      </div>
      <!-- Rows -->
      <div v-for="{ index, data: row } in list" :key="index" class="row">
        <div
          v-for="column in columns"
          :key="column.prop"
          class="cell"
          :style="column.width !== 0 ? `flex: 0 0 auto; width: ${column.width}px` : ''"
        >
          <slot :column="column" :row="row">{{ row[column.prop] }}</slot>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="less">
@prefix-cls: ~'@{namespace}-virt-table';

.dark .@{prefix-cls}-table {
  --table-row-bg-color: var(--el-fill-color-blank);
  --table-header-bg-color: var(--el-bg-color);
}

.@{prefix-cls}-table {
  --table-border-color: var(--el-border-color-lighter);
  --table-border: 1px solid var(--table-border-color);

  --table-row-bg-color: var(--el-fill-color-blank);
  --table-header-bg-color: var(--el-fill-color-light);

  width: 100%;
  overflow-y: scroll;
  display: inline-block;
  border-bottom: var(--table-border);

  .header {
    display: flex;
    position: sticky;
    top: 0;

    .cell {
      background: var(--table-header-bg-color);

      border-top: var(--table-border);
    }
  }

  .row {
    display: flex;
  }

  .cell {
    flex: 1 1 0%;
    height: 28px;
    padding: 3px;

    background: var(--table-row-bg-color);

    border-right: var(--table-border);
    border-bottom: var(--table-border);
  }
  .cell:first-child {
    border-left: var(--table-border);
  }

  &::-webkit-scrollbar {
    width: 6px;
    height: 6px;
  }
  &::-webkit-scrollbar-track {
    border-radius: 10px;
    background: rgba(0, 0, 0, 0.1);
  }
  &::-webkit-scrollbar-thumb {
    border-radius: 10px;
    background: rgba(0, 0, 0, 0.2);
  }
  &::-webkit-scrollbar-thumb:hover {
    background: rgba(0, 0, 0, 0.4);
  }
  &::-webkit-scrollbar-thumb:active {
    background: rgba(0, 0, 0, 0.6);
  }
}
</style>
