<script setup lang="ts">
import { ref } from 'vue'

import request from '@/api/utils/request'
import { ContentWrap } from '@/components/ContentWrap'
import { Columns, useRestoreScrollPositionInTable, VirtTable } from '@/components/VirtTable'
import { onLoadDataType } from '@/components/VirtTable/src/types'
import { fixed3Formatter, formatterArray, formatterDate } from '@/utils/formatter'

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
    { prop: 'control_id', type: 'number', label: '№', sort: 'ASC' },
    { prop: 'date_control', type: 'date', label: 'Дата', formatter: formatterDate },
    { prop: 'mark', type: 'string', label: 'Марка' },
    { prop: 'alternative_mark', type: 'string', label: 'Альт марка' },
    { prop: 'customers_name', type: 'string[]', label: 'Потребитель', formatter: formatterArray },
    {
      prop: 'volume_sum',
      type: 'number',
      label: 'Объем',
      align: 'right',
      formatter: fixed3Formatter
    },
    { prop: 'brigadier', type: 'string', label: 'Бригадир' },
    { prop: 'manufacturer', type: 'string', label: 'Изготовил' }
  )
)
const onLoadMore: onLoadDataType = async ({ page, size, sort, filters }) => {
  const { data } = await getData({
    page: JSON.stringify({ current: page, size }),
    sort: JSON.stringify(sort),
    filters: JSON.stringify(filters)
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
    />
  </content-wrap>
</template>
