<script setup lang="ts">
import { ContentWrap } from '@/components/ContentWrap'
import VirtualTable from './VirtualTable.vue'
import VirtualList from './VirtualList.vue'

// const generateColumns = (length = 10, prefix = 'column-') =>
//   Array.from({ length }).map((_, columnIndex) => ({
//     key: `${prefix}${columnIndex}`,
//     dataKey: `${prefix}${columnIndex}`,
//     label: `Column ${columnIndex}`,
//     width: 150
//   }))

// const generateData = (columns: ReturnType<typeof generateColumns>, length = 200, prefix = 'row-') =>
//   Array.from({ length }).map((_, rowIndex) => {
//     return columns.reduce(
//       (rowData, column, columnIndex) => {
//         rowData[column.dataKey] = `Row ${rowIndex} - Col ${columnIndex}`
//         return rowData
//       },
//       {
//         id: `${prefix}${rowIndex}`,
//         parentId: null
//       }
//     )
//   })

// const columns = generateColumns(10)
// const data = generateData(columns, 500)
</script>

<template>
  <content-wrap title="virtual-table" message="Таблица" class="mb-2">
    <virtual-table />
  </content-wrap>

  <content-wrap title="virtual-list" message="Лист">
    <virtual-list />
  </content-wrap>
</template>
