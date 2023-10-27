<script setup lang="ts">
import { UserSchemaBackend } from '@/api/generated'
import { getUsers } from '@/api/user'
import { ContentWrap } from '@/components/ContentWrap'
import { onMounted, onUpdated, ref } from 'vue'
import { userStatusKey } from './components/EventBusKey'
import { useEventBus } from '@vueuse/core'
import { loadingWrapper } from '@/utils/loading'
import RouterLinkToUserUpdate from '@/router/links/RouterLinkToUserUpdate.vue'
import RouterLinkToUserCreate from '@/router/links/RouterLinkToUserCreate.vue'

const users = ref<UserSchemaBackend[]>([])
const loading = ref(false)
let isNeedToUpdateTable = false

const loadData = loadingWrapper(loading, async () => {
  const { data } = await getUsers()
  users.value = data
})

onMounted(async () => {
  await loadData()
})

onUpdated(async () => {
  if (isNeedToUpdateTable) {
    isNeedToUpdateTable = false
    await loadData()
  }
})

const busUserStatus = useEventBus(userStatusKey)
busUserStatus.on(async () => {
  isNeedToUpdateTable = true
})
</script>

<template>
  <content-wrap style="height: calc(100vh - (35px + 50px + 2 * 20px + 5px))">
    <template #header>
      <router-link-to-user-create />
      <el-button class="ml-3" type="primary" @click="loadData">Обновить таблицу</el-button>
    </template>

    <el-table
      v-loading="loading"
      :data="users"
      border
      height="calc(100vh - (35px + 50px + 2 * 20px + 5px + 40px + 20px + 2 * 20px))"
    >
      <el-table-column prop="id" label="№" width="60">
        <template #default="{ row }"><router-link-to-user-update :user-id="row.id" /></template>
      </el-table-column>
      <el-table-column prop="username" label="Имя пользователя" />
      <el-table-column prop="surname" label="Фамилия" />
      <el-table-column prop="name" label="Имя" />
      <el-table-column prop="patronymic" label="Отчество" />
      <el-table-column prop="roles" label="Роли" show-overflow-tooltip>
        <template #default="{ row: { roles } }">{{ roles }}</template>
      </el-table-column>
      <el-table-column prop="avatar" label="Аватар" />
    </el-table>
  </content-wrap>
</template>
