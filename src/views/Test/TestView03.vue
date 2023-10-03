<script setup lang="ts">
import { ContentWrap } from '@/components/ContentWrap'
import { VirtTable } from '@/components/VirtTable'
import { Column } from '@/components/VirtTable/src/types'
import { ref } from 'vue'

const generateColumns = (length = 10, prefix = 'column-'): Column[] =>
  Array.from({ length }).map((_, columnIndex) => ({
    prop: `${prefix}${columnIndex}`,
    label: `Column ${columnIndex}`,
    width: 100
  }))

const generateData = (columns: Column[], length = 200) =>
  Array.from({ length }).map((_, rowIndex) => {
    return columns.reduce((rowData, column, columnIndex) => {
      rowData[column.prop] = `Row ${rowIndex} - Col ${columnIndex}`
      return rowData
    }, {})
  })

const columnTable = ref(generateColumns(15))
const dataTable = ref(generateData(columnTable.value, 100))
const onLoadMore = () => {
  dataTable.value.push(...generateData(columnTable.value, 100))
  console.log('onLoadMore')
}

const width = ref('100')
const test = () => {
  const _width = parseInt(width.value)

  columnTable.value[0].width = _width
  columnTable.value[5].width = _width
}
</script>

<template>
  <content-wrap
    title="virt-table"
    message="Таблица"
    style="height: calc(100vh - (35px + 50px + 2 * 20px + 5px))"
  >
    <el-input v-model="width" type="number" @change="test" />
    <el-button @click="test">test</el-button>
    <p>test</p>

    <virt-table
      :data="dataTable"
      :columns="columnTable"
      :on-load-more="onLoadMore"
      :height="'900px'"
    >
      <!-- <template #header="scope">{{ scope }}</template> -->
      <template #default="{ column: { prop }, row }">
        <template v-if="prop === 'column-0'"
          ><el-button>{{ row[prop] }}</el-button></template
        >
      </template>
    </virt-table>
  </content-wrap>
</template>
