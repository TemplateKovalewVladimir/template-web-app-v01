<script setup lang="ts">
import {
  ContextMenu,
  ContextMenuGroup,
  ContextMenuItem,
  ContextMenuSeparator
} from '@imengyu/vue3-context-menu'
import { computed, ref, Ref } from 'vue'
import { Column, Columns, SortType } from './types'
import { COLUMN_AUTO_WIDTH, COLUMN_MIN_WIDTH } from './types/constants'

const { columns } = defineProps<{
  columns: Columns
}>()

const emit = defineEmits<{
  (e: 'changeSort'): void
}>()

//////////////////////////////////////////////////////////////////////////////////////////
// Мутации Props!!!!
const setColumnWidth = (width: number): void => {
  if (columnCurrent.value?.width) columnCurrent.value.width = width
}
const setColumnVisible = (column: Column, visible: boolean): void => {
  column.visible = visible
}
const visibleAll = () => {
  columns.visibleAll()
}
const setSort = (sort: SortType) => {
  if (columnCurrent.value) {
    columns.resetSort()
    columnCurrent.value.sort = sort

    emit('changeSort')
  }
}
// Мутации Props!!!!
//////////////////////////////////////////////////////////////////////////////////////////

const contextMenuVisible = ref(false)
const contextMenuOptions = ref({ theme: 'virt-table', zIndex: 999, x: 0, y: 0 })

let columnCurrent: Ref<Column | null> = ref(null)
const isColumnAutoWidth: Ref<boolean> = ref(false)

const columnWidth = computed({
  set(value: number) {
    if (isColumnAutoWidth.value || value === null) return

    setColumnWidth(value)
  },
  get() {
    return columnCurrent.value?.width || 0
  }
})

const onVisibleAll = () => {
  visibleAll()
}
const onHideCurrent = () => {
  if (columnCurrent.value) setColumnVisible(columnCurrent.value, false)
}

const onAutoWidth = () => {
  isColumnAutoWidth.value = !isColumnAutoWidth.value
  setColumnWidth(isColumnAutoWidth.value ? COLUMN_AUTO_WIDTH : COLUMN_MIN_WIDTH)
}

const onShowContextMenu = (e: MouseEvent, column: Column) => {
  e.preventDefault()
  contextMenuVisible.value = true
  contextMenuOptions.value.x = e.x
  contextMenuOptions.value.y = e.y

  columnCurrent.value = column
  isColumnAutoWidth.value = column.width === COLUMN_AUTO_WIDTH
}

defineExpose({ onShowContextMenu })

const filters: Ref<any[]> = ref([])
const filterType = ref('')
const filterText = ref('')
const createFilter = () => {
  filters.value.push({ type: filterType.value, text: filterText.value })
  // contextMenuVisible.value = false
}
</script>

<template>
  <context-menu v-model:show="contextMenuVisible" :options="contextMenuOptions">
    <context-menu-item
      label="Сортировать"
      svg-icon="#icon-fluent-mdl2/sort-up"
      @click="setSort('ASC')"
    />
    <context-menu-item
      label="Сортировать"
      svg-icon="#icon-fluent-mdl2/sort-down"
      @click="setSort('DESC')"
    />

    <context-menu-separator />

    <context-menu-item
      label="Фильтры"
      svg-icon="#icon-fluent-mdl2/filter-settings"
      custom-class="no-hover"
      :click-close="false"
    >
      <template #label>
        <div class="flex flex-col">
          <el-select v-model="filterType" class="mb5px" :teleported="false">
            <el-option-group>
              <el-option value="Содержит" />
              <el-option value="Не содержит" />
            </el-option-group>
            <el-option-group>
              <el-option value="Равно" />
              <el-option value="Не равно" />
            </el-option-group>
            <el-option-group>
              <el-option value="Пусто" />
              <el-option value="Не пусто" />
            </el-option-group>
          </el-select>
          <el-input v-model="filterText" class="mb5px" />
          <el-button @click="createFilter">Применить</el-button>
        </div>
      </template>
    </context-menu-item>

    <context-menu-separator />

    <context-menu-item
      label="Сбросить фильтры"
      svg-icon="#icon-fluent-mdl2/clear-filter"
      :click-close="false"
    />

    <context-menu-separator v-if="filters.length > 0" />

    <context-menu-item
      v-for="(filter, index) of filters"
      :key="index"
      :label="`${filter.type}, ${filter.text}`"
      :click-close="false"
      svg-icon="#icon-ant-design/close-outlined"
    />

    <context-menu-separator />

    <context-menu-group label="Настройки" svg-icon="#icon-fluent-mdl2/column-options">
      <context-menu-item
        :label="'Автоширина ' + (isColumnAutoWidth ? '- ВЫКЛ' : '- ВКЛ')"
        svg-icon="#icon-fluent-mdl2/auto-fit-window"
        :click-close="false"
        @click="onAutoWidth"
      />
      <context-menu-item
        :click-close="false"
        :disabled="isColumnAutoWidth"
        custom-class="no-hover"
        svg-icon="#icon-fluent-mdl2/fit-width"
      >
        <template #label>
          <el-input-number
            v-model="columnWidth"
            :disabled="isColumnAutoWidth"
            :min="COLUMN_MIN_WIDTH"
            :max="1000"
            :step="5"
          />
        </template>
      </context-menu-item>

      <context-menu-separator />

      <context-menu-group label="Столбцы" svg-icon="#icon-fluent-mdl2/triple-column-edit">
        <context-menu-item
          label="Скрыть"
          svg-icon="#icon-fluent-mdl2/hide-3"
          @click="onHideCurrent"
        />
        <context-menu-item
          label="Показать все"
          svg-icon="#icon-fluent-mdl2/view"
          @click="onVisibleAll"
        />

        <context-menu-separator />

        <context-menu-item
          v-for="(column, index) of columns"
          :key="index"
          :svg-icon="column.visible ? '#icon-fluent-mdl2/view' : '#icon-fluent-mdl2/hide-3'"
          :label="column.label"
          :click-close="false"
          @click="setColumnVisible(column, !column.visible)"
        />
      </context-menu-group>
    </context-menu-group>
  </context-menu>
</template>

<style lang="less">
.mx-context-menu.virt-table {
  & {
    // --mx-menu-backgroud: #ffffff;
    --mx-menu-hover-backgroud: var(--el-color-primary-light-9);

    --mx-menu-hover-text: var(--el-color-primary);

    --mx-menu-open-backgroud: var(--el-color-primary-light-8);
    --mx-menu-open-hover-backgroud: var(--el-color-primary-light-7);
  }

  padding: 3px;
  border-radius: 4px;
  border: 1px solid var(--el-border-color-lighter);

  box-shadow: var(--el-box-shadow-light);

  .no-hover:hover {
    background-color: var(--mx-menu-backgroud);
  }

  .label {
    font-size: 12px;
    padding: 0;
  }

  .mx-context-menu-item {
    padding: 2px 5px;
    line-height: 20px;
    font-size: 12px;
  }

  .el-select-dropdown__item {
    height: 24px;
    line-height: 24px;
  }
  .el-select-group__wrap:not(:last-of-type) {
    padding-bottom: 8px;
  }
  .el-select-group__wrap:not(:last-of-type)::after {
    bottom: 4px;
  }
}
</style>
