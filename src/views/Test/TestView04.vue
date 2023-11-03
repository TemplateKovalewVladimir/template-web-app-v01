<script setup lang="ts">
import { ContentWrap } from '@/components/ContentWrap'
import { VirtTable, Columns, useRestoreScrollPositionInTable } from '@/components/VirtTable'
import { ref } from 'vue'
import request from '@/api/utils/request'
import { IColumnSort } from '@/components/VirtTable/src/types'

defineOptions({
  ...useRestoreScrollPositionInTable(['table1'])
})

function getData(query) {
  return request({
    url: '/refractory/',
    method: 'get',
    params: query
  })
}

const columnTable = ref(
  new Columns(
    { prop: 'control_id', type: 'number', label: 'id' },
    { prop: 'date_control', type: 'date', label: 'date_control' },
    { prop: 'recipe_id', type: 'number', label: 'recipe_id' },
    { prop: 'mark', type: 'string', label: 'mark' },
    { prop: 'customers_name', type: 'string', label: 'customers_name' },
    { prop: 'volume_sum', type: 'number', label: 'volume_sum' },
    { prop: 'brigadier', type: 'string', label: 'brigadier' },
    { prop: 'manufacturer', type: 'string', label: 'manufacturer' }
  )
)
const onLoadMore = async (current: number, size: number, sort: IColumnSort) => {
  const { data } = await getData({
    page: JSON.stringify({ current, size }),
    sort: JSON.stringify(sort)
  })
  return data
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
      :columns="columnTable"
      :on-load-data="onLoadMore"
      :virtual-list-overscan="50"
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
