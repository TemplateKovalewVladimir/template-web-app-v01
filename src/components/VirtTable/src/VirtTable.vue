<script setup lang="ts">
import { useVirtualList, useInfiniteScroll } from '@vueuse/core'
import { useDesign } from '@/hooks/web/useDesign'
import { PropType, computed, ref } from 'vue'

import { Column } from './types'
import { useScrollPosition } from './hooks/useScrollPosition'
import { useTooltip } from './hooks/useTooltip'
import VirtTableColumns from './VirtTableColumns.vue'
import VirtTableHeaderCell from './VirtTableHeaderCell.vue'

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
  },
  rowHeight: {
    type: Number,
    default: 28
  },

  virtualListOverscan: {
    type: Number,
    default: 10
  },
  infiniteScrollDistance: {
    type: Number,
    default: 10
  },

  tooltipShowDelay: {
    type: Number,
    default: 500
  }
})

// computed
const rowHeight = computed(() => `${props.rowHeight}px`)
const headerHeight = computed(() => `${props.rowHeight + 10}px`)

// Стили для css
const { getPrefixCls } = useDesign()
const prefixCls = getPrefixCls('virt-table')

// Виртуальный список
const { list, containerProps, wrapperProps } = useVirtualList(props.data, {
  itemHeight: props.rowHeight,
  overscan: props.virtualListOverscan
})

// Загрузка новых данных при scroll`е
const loadingData = ref(false)

useInfiniteScroll(
  containerProps.ref,
  async () => {
    loadingData.value = true
    await props.onLoadMore()
    loadingData.value = false
  },
  { distance: props.infiniteScrollDistance }
)

// tooltip
const {
  tooltipVisible,
  tooltipContent,
  tooltipTriggerRef,
  handleCellMouseEnter,
  handleCellMouseLeave
} = useTooltip(props.tooltipShowDelay)

// Scroll для vue-router
const { saveScrollPosition, restoreScrollPosition } = useScrollPosition(containerProps.ref)

defineExpose({ saveScrollPosition, restoreScrollPosition })
</script>

<template>
  <div v-loading="loadingData">
    <div v-bind="containerProps" :class="`${prefixCls}`" :style="`height: ${props.height}`">
      <!-- Header -->
      <div class="header">
        <virt-table-columns :columns="columns">
          <template #default="{ column }">
            <slot :name="'h-' + column.prop" :column="column">
              <virt-table-header-cell :column="column" />
            </slot>
          </template>
        </virt-table-columns>
      </div>

      <!-- Rows -->
      <div v-if="data.length !== 0" v-bind="wrapperProps">
        <div v-for="{ index, data: row } in list" :key="index" class="row">
          <virt-table-columns :columns="columns">
            <template #default="{ column }">
              <div
                class="text"
                @mouseenter="handleCellMouseEnter($event, column)"
                @mouseleave="handleCellMouseLeave($event, column)"
              >
                <slot :name="column.prop" :column="column" :row="row">{{ row[column.prop] }}</slot>
              </div>
            </template>
          </virt-table-columns>
        </div>
      </div>

      <!-- Empty -->
      <div v-else class="empty"><el-empty description="Нет данных" /></div>
    </div>
  </div>

  <el-tooltip
    v-model:visible="tooltipVisible"
    :content="tooltipContent"
    placement="top"
    virtual-triggering
    :virtual-ref="tooltipTriggerRef"
  />
</template>

<style lang="less">
@prefix-cls: ~'@{namespace}-virt-table';

.dark .@{prefix-cls} {
  --table-row-bg-color: var(--el-fill-color-blank);
  --table-header-bg-color: var(--el-fill-color-light);

  --scrollbar-track-bg-color: rgba(255, 255, 255, 0.1);
  --scrollbar-thumb-bg-color: rgba(255, 255, 255, 0.2);
  --scrollbar-thumb-hover-bg-color: rgba(255, 255, 255, 0.4);
  --scrollbar-thumb-active-bg-color: rgba(255, 255, 255, 0.6);
}

.@{prefix-cls} {
  --table-border-color: var(--el-border-color-lighter);
  --table-border: 1px solid var(--table-border-color);

  --table-row-bg-color: var(--el-fill-color-blank);
  --table-header-bg-color: var(--el-fill-color-light);

  --scrollbar-track-bg-color: rgba(0, 0, 0, 0.1);
  --scrollbar-thumb-bg-color: rgba(0, 0, 0, 0.2);
  --scrollbar-thumb-hover-bg-color: rgba(0, 0, 0, 0.4);
  --scrollbar-thumb-active-bg-color: rgba(0, 0, 0, 0.6);

  color: var(--el-text-color-regular);
  font-size: 14px;
  width: 100%;
  overflow-y: scroll;
  border: var(--table-border);

  .empty {
    display: flex;
    justify-content: center;
    align-items: center;
    height: calc(100% - v-bind('headerHeight'));

    font-size: 24px;
  }

  .header {
    display: flex;
    position: sticky;
    top: 0;

    color: var(--el-text-color-secondary);
    font-weight: 600;

    .cell {
      height: v-bind('headerHeight');
      line-height: v-bind('headerHeight');

      background: var(--table-header-bg-color);
    }
  }

  .row {
    display: flex;
  }

  .cell {
    flex: 1 1 0%;
    min-width: 50px;

    height: v-bind('rowHeight');
    line-height: v-bind('rowHeight');
    padding: 0 5px;

    box-sizing: border-box;

    background: var(--table-row-bg-color);

    border-right: var(--table-border);
    border-bottom: var(--table-border);

    div.text {
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
  }
  .cell:last-child {
    border-right: none;
  }

  // Scroll
  &::-webkit-scrollbar {
    width: 6px;
    height: 6px;
  }
  &::-webkit-scrollbar-corner {
    background: transparent;
    border-right: var(--table-border);
  }
  &::-webkit-scrollbar-track {
    border-radius: 10px;
    background: var(--scrollbar-track-bg-color);
  }
  &::-webkit-scrollbar-thumb {
    border-radius: 10px;
    background: var(--scrollbar-thumb-bg-color);
  }
  &::-webkit-scrollbar-thumb:hover {
    background: var(--scrollbar-thumb-hover-bg-color);
  }
  &::-webkit-scrollbar-thumb:active {
    background: var(--scrollbar-thumb-active-bg-color);
  }
}
</style>
