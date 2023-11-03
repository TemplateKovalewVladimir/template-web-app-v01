<script setup lang="ts">
import { ContentWrap } from '@/components/ContentWrap'
import {
  VirtTable,
  Columns,
  IColumn,
  useRestoreScrollPositionInTable
} from '@/components/VirtTable'
import { ref } from 'vue'

defineOptions({
  ...useRestoreScrollPositionInTable(['table1'])
})

// eslint-disable-next-line @typescript-eslint/no-unused-vars
function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms))
}

const generateColumns = (length = 10, prefix = 'column-'): Columns => {
  const c: IColumn[] = Array.from({ length }).map((_, columnIndex) => ({
    prop: `${prefix}${columnIndex}`,
    label: `Column ${columnIndex}`,
    type: 'string'
  }))

  return new Columns(...c)
}

const generateData = (columns: Columns, length = 200) =>
  Array.from({ length }).map((_, rowIndex) => {
    return columns.reduce((rowData, column, columnIndex) => {
      rowData[column.prop] = `Row ${rowIndex} - Col ${columnIndex}`
      return rowData
    }, {})
  })

const columnTable = ref(generateColumns(15))
const onLoadMore = async () => {
  await sleep(200)
  return generateData(columnTable.value, 100)
}
</script>

<template>
  <content-wrap
    title="virtual-table"
    message="Таблица"
    style="height: calc(100vh - (35px + 50px + 2 * 20px + 5px))"
  >
    <virt-table
      ref="table1"
      :virtual-list-overscan="50"
      :columns="columnTable"
      :on-load-data="onLoadMore"
      height="calc(100vh - (35px + 50px + 2 * 20px + 5px + 100px))"
    >
      <template #h-column-0="{ column }">
        <div class="text">{{ column }}</div>
      </template>

      <template #column-0="{ row }">
        <el-button>{{ row['column-0'] }}</el-button>
      </template>
    </virt-table>
  </content-wrap>
</template>
