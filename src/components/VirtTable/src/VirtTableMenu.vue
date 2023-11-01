<script setup lang="ts">
import {
  ContextMenu,
  ContextMenuGroup,
  ContextMenuItem,
  ContextMenuSeparator
} from '@imengyu/vue3-context-menu'
import { computed, ref, Ref } from 'vue'
import { Column } from './types'
import { COLUMN_AUTO_WIDTH, COLUMN_MIN_WIDTH } from './types/constants'

const { columns } = defineProps<{
  columns: Column[]
}>()

//////////////////////////////////////////////////////////////////////////////////////////
// Мутации Props!!!!
const setColumnWidth = (width: number): void => {
  if (columnCurrent.value?.width) columnCurrent.value.width = width
}
const setColumnVisible = (column: Column, visible: boolean): void => {
  column.visible = visible
}
// Мутации Props!!!!
//////////////////////////////////////////////////////////////////////////////////////////

const contextMenuVisible = ref(false)
const contextMenuOptions = ref({ theme: 'virt-table', zIndex: 3, x: 0, y: 0 })

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
</script>

<template>
  <context-menu v-model:show="contextMenuVisible" :options="contextMenuOptions">
    <context-menu-item label="Сортировать" svg-icon="#icon-fluent-mdl2/sort-up" />
    <context-menu-item label="Сортировать" svg-icon="#icon-fluent-mdl2/sort-down" />

    <context-menu-separator />

    <context-menu-item label="Фильтры" svg-icon="#icon-fluent-mdl2/filter-settings" />
    <context-menu-item label="Сбросить фильтры" svg-icon="#icon-fluent-mdl2/clear-filter" />

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
  border: 1px solid var(--mx-menu-border-color);

  box-shadow: var(--el-box-shadow-light);

  .label {
    font-size: 12px;
    padding: 0;
  }

  .mx-context-menu-item {
    padding: 2px 5px;
    line-height: 20px;
    font-size: 12px;
  }
}
</style>
