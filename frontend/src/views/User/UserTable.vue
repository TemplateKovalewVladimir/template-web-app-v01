<script setup lang="ts">
import { useEventBus } from '@vueuse/core'
import { onUpdated, ref } from 'vue'

import { getUsers } from '@/api/user'
import { ContentWrap } from '@/components/ContentWrap'
import { Columns, useRestoreScrollPositionInTable, VirtTable } from '@/components/VirtTable'
import { VirtTableType } from '@/components/VirtTable/src/types'
import RouterLinkToUserCreate from '@/router/links/RouterLinkToUserCreate.vue'
import RouterLinkToUserUpdate from '@/router/links/RouterLinkToUserUpdate.vue'
import { tableHeightWrappedInContentWrapInHeaderButton } from '@/utils/constants'

import { userStatusKey } from './components/EventBusKey'

defineOptions({
  ...useRestoreScrollPositionInTable(['tableUserRef'])
})

const tableUserRef = ref<VirtTableType | null>(null)

const columnUserTable = ref(
  new Columns(
    { prop: 'id', type: 'number', label: '№', sort: 'DESC' },
    { prop: 'username', type: 'string', label: 'Логин' },
    { prop: 'surname', type: 'string', label: 'Фамилия' },
    { prop: 'name', type: 'string', label: 'Имя' },
    { prop: 'patronymic', type: 'string', label: 'Отчество' },
    { prop: 'roles', type: 'string', label: 'Роли', menu: false }
  )
)

const onLoadUser = async ({ page, size, sort, filters }) => {
  const { data } = await getUsers({ page, size, sort, filters })
  return data
}

// Обработка обновления таблицы при изменении пользователей
let isNeedToUpdateTable = false
onUpdated(async () => {
  if (isNeedToUpdateTable) {
    isNeedToUpdateTable = false
    tableUserRef.value?.reloadData()
  }
})
const busUserStatus = useEventBus(userStatusKey)
busUserStatus.on(async () => {
  isNeedToUpdateTable = true
})
</script>

<template>
  <content-wrap>
    <template #header>
      <router-link-to-user-create />
      <el-button class="ml-3" type="primary" @click="tableUserRef?.reloadData()"
        >Обновить таблицу</el-button
      >
    </template>

    <virt-table
      ref="tableUserRef"
      :columns="columnUserTable"
      :on-load-data="onLoadUser"
      :height="tableHeightWrappedInContentWrapInHeaderButton"
    >
      <template #id="{ row }"><router-link-to-user-update :user-id="row.id" /></template
    ></virt-table>
  </content-wrap>
</template>
