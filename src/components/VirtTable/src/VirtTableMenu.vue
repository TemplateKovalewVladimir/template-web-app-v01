<script setup lang="ts">
import {
  ContextMenu,
  ContextMenuGroup,
  ContextMenuItem,
  ContextMenuSeparator
} from '@imengyu/vue3-context-menu'
import { Icon } from '@/components/Icon'
import { ref, Ref, watch } from 'vue'
import { Column } from './types'

const { columns } = defineProps<{
  columns: Column[]
}>()

const contextMenuVisible = ref(false)
const contextMenuOptions = ref({
  zIndex: 3,
  theme: 'virt-table',
  // minWidth: 230,
  x: 500,
  y: 200
})

const columnWidth: Ref<number> = ref(0)
let columnCurrent: Column | null = null

watch(columnWidth, (newWidth, oldWidth) => {
  if (columnCurrent?.width) {
    if (oldWidth === -1 && newWidth === 4) columnWidth.value = 50
    columnCurrent.width = columnWidth.value
  }
})

const onShowContextMenu = (e: MouseEvent, column: Column) => {
  e.preventDefault()
  contextMenuVisible.value = true
  contextMenuOptions.value.x = e.x
  contextMenuOptions.value.y = e.y

  columnCurrent = column
  columnWidth.value = column.width
}

defineExpose({ onShowContextMenu })
</script>

<template>
  <context-menu v-model:show="contextMenuVisible" :options="contextMenuOptions">
    <context-menu-item label="Сортировать">
      <template #icon><icon icon="fluent-mdl2/sort-up" :size="14" /></template>
    </context-menu-item>
    <context-menu-item label="Сортировать">
      <template #icon><icon icon="fluent-mdl2/sort-down" :size="14" /></template>
    </context-menu-item>

    <context-menu-separator />

    <context-menu-item label="Фильтры">
      <template #icon><icon icon="fluent-mdl2/filter-settings" :size="14" /></template>
    </context-menu-item>
    <context-menu-item label="Сбросить фильтры">
      <template #icon><icon icon="fluent-mdl2/clear-filter" :size="14" /></template>
    </context-menu-item>

    <context-menu-separator />

    <context-menu-group label="Настройки" icon="sd">
      <context-menu-item label="Item1" />
      <context-menu-item :click-close="false">
        <template #label><el-input-number v-model="columnWidth" :step="5" /></template>
      </context-menu-item>
      <context-menu-group label="Child">
        <context-menu-item
          v-for="(column, index) of columns"
          :key="index"
          :click-close="false"
          @click="column.visible = !column.visible"
        >
          <template #icon>
            <icon :icon="column.visible ? 'el/eye-open' : 'el/eye-close'" :size="14" />
          </template>
          <template #label>{{ column.label }}</template>
        </context-menu-item>
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
  }

  .mx-context-menu-item {
    padding: 2px 5px;
    line-height: 20px;
    font-size: 12px;
  }
}
</style>
