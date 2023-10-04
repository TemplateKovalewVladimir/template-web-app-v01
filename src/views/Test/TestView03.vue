<script setup lang="ts">
import { ContentWrap } from '@/components/ContentWrap'
import { VirtTable } from '@/components/VirtTable'
import { Column } from '@/components/VirtTable/src/types'
import { ref } from 'vue'

// eslint-disable-next-line @typescript-eslint/no-unused-vars
function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms))
}

const generateColumns = (length = 10, prefix = 'column-'): Column[] =>
  Array.from({ length }).map((_, columnIndex) => ({
    prop: `${prefix}${columnIndex}`,
    label: `Column ${columnIndex}`,
    width: columnIndex === 0 ? 0 : 100
  }))

const generateData = (columns: Column[], length = 200) =>
  Array.from({ length }).map((_, rowIndex) => {
    return columns.reduce((rowData, column, columnIndex) => {
      rowData[column.prop] = `Row ${rowIndex} - Col ${columnIndex}`
      return rowData
    }, {})
  })

const columnTable = ref(generateColumns(5))
const dataTable = ref(generateData(columnTable.value, 100))
const onLoadMore = async () => {
  await sleep(200)
  dataTable.value.push(...generateData(columnTable.value, 100))
}

const width = ref('100')
const test = () => {
  const _width = parseInt(width.value)

  columnTable.value[0].width = _width
  columnTable.value[5].width = _width
}

const rowHeight = ref('28')
</script>

<template>
  <content-wrap
    title="virt-table"
    message="Таблица"
    style="height: calc(100vh - (35px + 50px + 2 * 20px + 5px))"
  >
    <el-input v-model="width" type="number" @change="test" />
    <el-input v-model="rowHeight" type="number" />
    <p>test</p>

    <virt-table
      :data="dataTable"
      :columns="columnTable"
      :on-load-more="onLoadMore"
      :height="'900px'"
      :row-height="parseInt(rowHeight)"
    >
      <template #header="{ column: { label } }">{{ label }}</template>
      <template #default="{ column: { prop }, row }">
        <template v-if="prop === 'column-0'"
          ><el-button>{{ row[prop] }}</el-button></template
        >
      </template>
    </virt-table>
  </content-wrap>
</template>
