<script setup lang="ts">
import { useVirtualList, useInfiniteScroll } from '@vueuse/core'
import { ref } from 'vue'

const generateColumns = (length = 10, prefix = 'column-') =>
  Array.from({ length }).map((_, columnIndex) => ({
    index: columnIndex,
    key: `${prefix}${columnIndex}`,
    dataKey: `${prefix}${columnIndex}`,
    label: `Column ${columnIndex}`,
    width: 150
  }))

const generateData = (columns: ReturnType<typeof generateColumns>, length = 200, prefix = 'row-') =>
  Array.from({ length }).map((_, rowIndex) => {
    return columns.reduce(
      (rowData, column, columnIndex) => {
        rowData[column.dataKey] = `Row ${rowIndex} - Col ${columnIndex}`
        return rowData
      },
      {
        id: `${prefix}${rowIndex}`,
        parentId: null
      }
    )
  })

const columns = ref(generateColumns(10))

const allItems = ref(generateData(columns.value, 100))

const { list, containerProps, wrapperProps } = useVirtualList(allItems, {
  itemHeight: 28,
  overscan: 10
})

useInfiniteScroll(
  containerProps.ref,
  async () => {
    allItems.value.push(...generateData(columns.value, 100))
  },
  { distance: 10 }
)

const testClick = () => {
  allItems.value[5]['column-1'] = 'rrr'

  columns.value[0].label = 'test'
  columns.value[0].width = 100
  columns.value[1].width = 0

  // const tmp = columns[0]
  // columns[0] = columns[1]
  // columns[1] = tmp

  console.log(columns)
}
</script>

<template>
  <el-button @click="testClick">test</el-button>
  <h2>length: {{ allItems.length }}</h2>
  <div class="h-150px">
    <div>{{ containerProps }}</div>
    <div>{{ wrapperProps }}</div>
    <!-- <div>{{ list }}</div> -->
  </div>

  <div v-bind="containerProps" class="my-table h-300px">
    <div v-bind="wrapperProps">
      <div class="header">
        <!-- Header columns -->
        <div
          v-for="column in columns"
          :key="column.key"
          class="cell"
          :style="column.width !== 0 ? `flex: 0 0 auto; width: ${column.width}px` : ''"
        >
          {{ column.label }}
        </div>
      </div>
      <!-- Rows -->
      <div v-for="{ index, data: row } in list" :key="index" class="row">
        <div
          v-for="column in columns"
          :key="column.key"
          class="cell"
          :style="column.width !== 0 ? `flex: 0 0 auto; width: ${column.width}px` : ''"
        >
          {{ column.index === 0 ? index : row[column.key] }}
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="less">
.my-table {
  width: 100%;
  overflow-y: scroll;
  display: inline-block;

  .header {
    display: flex;
    position: sticky;
    top: 0;
  }

  .row {
    display: flex;
  }

  .cell {
    flex: 1 1 0%;
    height: 28px;
    background: white;
  }

  &::-webkit-scrollbar {
    width: 6px;
    height: 6px;
  }
  &::-webkit-scrollbar-track {
    border-radius: 10px;
    background: rgba(0, 0, 0, 0.1);
  }
  &::-webkit-scrollbar-thumb {
    border-radius: 10px;
    background: rgba(0, 0, 0, 0.2);
  }
  &::-webkit-scrollbar-thumb:hover {
    background: rgba(0, 0, 0, 0.4);
  }
  &::-webkit-scrollbar-thumb:active {
    background: rgba(0, 0, 0, 0.6);
  }
}
</style>
