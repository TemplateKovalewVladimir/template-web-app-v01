<script setup lang="ts">
import { ContentWrap } from '@/components/ContentWrap'

const generateColumns1 = (length = 10, prefix = 'column-') =>
  Array.from({ length }).map((_, columnIndex) => ({
    key: `${prefix}${columnIndex}`,
    dataKey: `${prefix}${columnIndex}`,
    title: `Column ${columnIndex}`,
    width: 150
  }))

const generateData1 = (
  columns: ReturnType<typeof generateColumns1>,
  length = 200,
  prefix = 'row-'
) =>
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

const generateColumns2 = (length = 10, prefix = 'column-') =>
  Array.from({ length }).map((_, columnIndex) => ({
    key: `${prefix}${columnIndex}`,
    dataKey: `${prefix}${columnIndex}`,
    title: `Column ${columnIndex}`,
    width: 150
  }))

const generateData2 = (
  columns: ReturnType<typeof generateColumns2>,
  length = 200,
  prefix = 'row-'
) =>
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

const columns1 = generateColumns1(3)
const data1 = generateData1(columns1, 500)

const columns2 = generateColumns2(3)
const data2 = generateData2(columns2, 100000)
</script>

<template>
  <el-row :gutter="10">
    <el-col :span="12">
      <content-wrap title="el-table" message="Первая версия">
        <el-table border :data="data1" :max-height="500">
          <el-table-column
            v-for="(column, i) in columns1"
            :key="i"
            :label="column.title"
            :prop="column.dataKey"
          />
        </el-table>
      </content-wrap>
    </el-col>
    <el-col :span="12">
      <content-wrap title="el-table-v2" message="Вторая версия">
        <el-table-v2 border :columns="columns2" :data="data2" :width="700" :height="400" fixed />
      </content-wrap>
    </el-col>
  </el-row>
</template>
