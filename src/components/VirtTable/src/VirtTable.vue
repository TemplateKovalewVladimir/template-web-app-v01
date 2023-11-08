<script setup lang="ts">
import { useDesign } from '@/hooks/web/useDesign'
import { PropType, computed, ref } from 'vue'

import { Column, Columns, onLoadDataType } from './types'
import { COLUMN_MIN_WIDTH } from './types/constants'
import { useScrollPosition } from './hooks/useScrollPosition'
import { useTooltip } from './hooks/useTooltip'
import VirtTableRow from './VirtTableRow.vue'
import VirtTableHeaderCell from './VirtTableHeaderCell.vue'
import VirtTableMenu from './VirtTableMenu.vue'
import { useVirtualData } from './hooks/useVirtualData'

const props = defineProps({
  /**
   * Список колонок для отображения в таблице (обязательный параметр).
   */
  columns: {
    type: Columns,
    required: true
  },
  /**
   * Функция, которая вызывается при загрузке данных (обязательный параметр).
   */
  onLoadData: {
    type: Function as PropType<onLoadDataType>,
    required: true
  },
  /**
   * Кол-во строк в одной странице
   */
  sizePage: {
    type: Number,
    default: 100
  },

  /**
   * Высота таблицы (по умолчанию '300px').
   */
  height: {
    type: String,
    default: '300px'
  },
  /**
   * Высота строки таблицы (по умолчанию 28).
   */
  rowHeight: {
    type: Number,
    default: 28
  },

  /**
   * Количество "лишних" элементов виртуального списка (по умолчанию 10).
   */
  virtualListOverscan: {
    type: Number,
    default: 10
  },
  /**
   * Расстояние до нижней части таблицы, когда начинается бесконечная прокрутка (по умолчанию 10)
   */
  infiniteScrollDistance: {
    type: Number,
    default: 10
  },

  /**
   * Задержка перед показом всплывающей подсказки (по умолчанию 500 миллисекунд).
   */
  tooltipShowDelay: {
    type: Number,
    default: 500
  }
})

// computed
const rowHeight = computed(() => `${props.rowHeight}px`)
const headerHeight = computed(() => `${props.rowHeight + 10}px`)
const columnMinWidth = computed(() => `${COLUMN_MIN_WIDTH}px`)

// Стили для css
const { getPrefixCls } = useDesign()
const prefixCls = getPrefixCls('virt-table')

// Виртуальный список & Загрузка новых данных при scroll`е
const {
  loading,
  data,
  reloadData,
  currentPage,
  virtualData,
  virtualContainerProps,
  virtualWrapperProps
} = useVirtualData(
  props.onLoadData,
  props.columns,
  props.sizePage,
  props.rowHeight,
  props.virtualListOverscan,
  props.infiniteScrollDistance
)

// Scroll для vue-router
const { saveScrollPosition, restoreScrollPosition } = useScrollPosition(virtualContainerProps.ref)

// tooltip
const {
  tooltipVisible,
  tooltipContent,
  tooltipTriggerRef,
  handleCellMouseEnter,
  handleCellMouseLeave
} = useTooltip(props.tooltipShowDelay)

// Контекстное меню
const virtTableMenu = ref<InstanceType<typeof VirtTableMenu> | null>(null)
const onShowContextMenu = (e: MouseEvent, column: Column) => {
  virtTableMenu.value?.onShowContextMenu(e, column)
}

// Expose
defineExpose({ saveScrollPosition, restoreScrollPosition })
</script>

<template>
  <div v-loading="loading">
    <div v-bind="virtualContainerProps" :class="`${prefixCls}`" :style="`height: ${props.height}`">
      <!-- Header -->
      <div class="header">
        <virt-table-row :columns="columns" @contextmenu="onShowContextMenu">
          <template #default="{ column }">
            <slot :name="'h-' + column.prop" :column="column">
              <virt-table-header-cell :column="column" />
            </slot>
          </template>
        </virt-table-row>
      </div>

      <!-- Rows -->
      <div v-if="data.length !== 0" v-bind="virtualWrapperProps">
        <div v-for="{ index, data: row } in virtualData" :key="index" class="row">
          <virt-table-row :columns="columns">
            <template #default="{ column }">
              <div
                class="text"
                @mouseenter="handleCellMouseEnter($event, column)"
                @mouseleave="handleCellMouseLeave($event, column)"
              >
                <slot :name="column.prop" :column="column" :row="row">{{ row[column.prop] }}</slot>
              </div>
            </template>
          </virt-table-row>
        </div>
      </div>

      <!-- Empty -->
      <div v-else class="empty"><el-empty description="Нет данных" /></div>
    </div>
  </div>
  <div class="text-8px float-right color-gray mt3px">
    <span>Page: {{ currentPage }} | </span>
    <span>Count: {{ data.length }} | </span>
    <span>Count virtual: {{ virtualData.length }} | </span>
    <span>Size: {{ sizePage }}</span>
  </div>

  <el-tooltip
    v-model:visible="tooltipVisible"
    :content="tooltipContent"
    placement="top"
    virtual-triggering
    :virtual-ref="tooltipTriggerRef"
  />

  <virt-table-menu
    ref="virtTableMenu"
    :columns="columns"
    @change-sort="reloadData"
    @change-filter="reloadData"
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
    min-width: v-bind('columnMinWidth');

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
