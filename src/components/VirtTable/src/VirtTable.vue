<script setup lang="ts">
import { debounce } from 'lodash-es'
import { useVirtualList, useInfiniteScroll } from '@vueuse/core'
import { useDesign } from '@/hooks/web/useDesign'
import { PropType, computed, ref } from 'vue'

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

const rowHeight = computed(() => `${props.rowHeight}px`)
const headerHeight = computed(() => `${props.rowHeight}px`)

// #region Стили для css
const { getPrefixCls } = useDesign()
const prefixCls = getPrefixCls('virt-table')
// #endregion

// #region Виртуальный список
const { list, containerProps, wrapperProps } = useVirtualList(props.data, {
  itemHeight: props.rowHeight,
  overscan: props.virtualListOverscan
})
// #endregion

// #region Загрузка новых данных при scroll`е
useInfiniteScroll(
  containerProps.ref,
  () => {
    props.onLoadMore()
  },
  { distance: props.infiniteScrollDistance }
)
// #endregion

// #region tooltip
const tooltipPosition = ref({
  height: 0,
  width: 0,
  x: 0,
  y: 0,
  top: 0,
  right: 0,
  bottom: 0,
  left: 0,
  toJSON() {}
})
const tooltipContent = ref('')
const tooltipVisible = ref(false)
const tooltipTriggerRef = ref({
  getBoundingClientRect() {
    return tooltipPosition.value
  }
})

const tooltipVisibility = (action: 'show' | 'hide', content = '') => {
  if (action === 'hide') {
    tooltipVisible.value = false
    return
  }
  tooltipContent.value = content
  tooltipVisible.value = true
}
const debouncedTooltipVisibility = debounce(tooltipVisibility, props.tooltipShowDelay)

const handleCellMouseEnter = (event: MouseEvent, column: Column) => {
  if (column.showOverflowTooltip === false) return
  const cell = event.target as HTMLElement
  if (cell && cell.clientWidth < cell.scrollWidth) {
    tooltipPosition.value = cell.getBoundingClientRect()

    if (cell.textContent) debouncedTooltipVisibility('show', cell.textContent)
  }
}

const handleCellMouseLeave = (_event: MouseEvent, column: Column) => {
  if (column.showOverflowTooltip === false) return
  tooltipVisibility('hide')
  debouncedTooltipVisibility('hide')
}
// #endregion
</script>

<template>
  <div v-bind="containerProps" :class="`${prefixCls}`" :style="`height: ${props.height}`">
    <div class="header">
      <!-- Header columns -->
      <div
        v-for="column in columns"
        :key="column.prop"
        class="cell"
        :style="column.width !== 0 ? `flex: 0 0 auto; width: ${column.width}px` : ''"
      >
        <div
          ><slot name="header" :column="column">{{ column.label }}</slot></div
        >
      </div>
    </div>
    <!-- Rows -->
    <div v-bind="wrapperProps">
      <div v-for="{ index, data: row } in list" :key="index" class="row">
        <div
          v-for="column in columns"
          :key="column.prop"
          class="cell"
          :style="column.width !== 0 ? `flex: 0 0 auto; width: ${column.width}px` : ''"
        >
          <div
            @mouseenter="handleCellMouseEnter($event, column)"
            @mouseleave="handleCellMouseLeave($event, column)"
            ><slot :column="column" :row="row">{{ row[column.prop] }}</slot></div
          >
        </div>
      </div>
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
  border-bottom: var(--table-border);

  .header {
    display: flex;
    position: sticky;
    top: 0;

    color: var(--el-text-color-secondary);
    font-weight: 600;

    .cell {
      height: v-bind('headerHeight');
      line-height: v-bind('headerHeight');

      border-top: var(--table-border);
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

    div {
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
  }
  .cell:first-child {
    border-left: var(--table-border);
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
