<script setup lang="ts">
import { ref } from 'vue'

import { getQueryPaginateSortFilters, request } from '@/api/utils/request'
import { ContentWrap } from '@/components/ContentWrap'
import { Columns, useRestoreScrollPositionInTable, VirtTable } from '@/components/VirtTable'
import { onLoadDataType, VirtTableType } from '@/components/VirtTable/src/types'
import { useCan } from '@/hooks/web/useCan'
import { tableHeightWrappedInContentWrapInHeader } from '@/utils/constants'
import { fixed3Formatter, formatterArray, formatterDate } from '@/utils/formatter'

defineOptions({
  ...useRestoreScrollPositionInTable(['table1'])
})

const { isCan } = useCan()

const table1 = ref<VirtTableType | null>(null)

function getData(query) {
  return request({
    url: '/refractory/',
    method: 'get',
    params: query
  })
}

const columnTable = ref(
  new Columns(
    { prop: '_check', type: 'number', label: '', width: 25, menu: false },
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
const onLoadMore: onLoadDataType = async ({ page, size, sort, filters }) =>
  (await getData(getQueryPaginateSortFilters({ page, size, sort, filters }))).data

const tetsInput = ref('asd')
</script>

<template>
  <content-wrap title="virtual - table" message="Таблица">
    <el-button :disabled="!isCan">test123</el-button>
    <el-input v-model="tetsInput" :disabled="!isCan"></el-input>

    <el-form-item label="13">
      <el-input v-model="tetsInput" :disabled="!isCan"></el-input>
    </el-form-item>
    <virt-table
      ref="table1"
      :columns="columnTable"
      :on-load-data="onLoadMore"
      :virtual-list-overscan="50"
      :height="tableHeightWrappedInContentWrapInHeader"
    >
      <template #_check><el-checkbox /></template>
    </virt-table>
  </content-wrap>
</template>
