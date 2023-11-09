<script setup lang="ts">
import { ref } from 'vue'

import { ContentWrap } from '@/components/ContentWrap'
import {
  Column,
  Columns,
  IColumn,
  useRestoreScrollPositionInTable,
  VirtTable
} from '@/components/VirtTable'

defineOptions({
  ...useRestoreScrollPositionInTable(['table1', 'table2'])
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

const generateData = (columns: Column[], length = 200) =>
  Array.from({ length }).map((_, rowIndex) => {
    return columns.reduce((rowData, column, columnIndex) => {
      rowData[column.prop] = `Row ${rowIndex} - Col ${columnIndex}`
      return rowData
    }, {})
  })

const columnTable = ref(generateColumns(5))
const onLoadMore = async () => {
  await sleep(200)
  return generateData(columnTable.value, 100)
}

const width = ref('100')
const test = () => {
  const _width = parseInt(width.value)

  columnTable.value[0].width = _width
  // columnTable.value[5].width = _width
}

const rowHeight = ref('28')
</script>

<template>
  <content-wrap
    title="virt-table"
    message="Таблица"
    style="height: calc(100vh - (35px + 50px + 2 * 20px + 5px))"
  >
    <el-row :gutter="20">
      <el-col :span="12">
        <el-input v-model="width" type="number" @change="test" />
        <el-input v-model="rowHeight" type="number" />
        <p>test</p>

        <virt-table
          ref="table1"
          :columns="columnTable"
          :on-load-data="onLoadMore"
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
      </el-col>
      <el-col :span="12">
        <el-input v-model="width" type="number" @change="test" />
        <el-input v-model="rowHeight" type="number" />
        <p>test</p>

        <virt-table
          ref="table2"
          :columns="columnTable"
          :on-load-data="onLoadMore"
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
      </el-col>
    </el-row>
  </content-wrap>
</template>
