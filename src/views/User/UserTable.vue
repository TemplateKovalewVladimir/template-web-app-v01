<script setup lang="ts">
import { UserSchemaBackend } from '@/api/generated'
import { getUsers } from '@/api/user'
import { ContentWrap } from '@/components/ContentWrap'
import { onMounted, ref } from 'vue'
import { userStatusKey } from './EventBusKey'
import { useEventBus } from '@vueuse/core'

const users = ref<UserSchemaBackend[]>([])
const loading = ref(false)
onMounted(async () => {
  loading.value = true
  const { data } = await getUsers()
  users.value = data
  loading.value = false
})

const busUserStatus = useEventBus(userStatusKey)
busUserStatus.on((event) => {
  console.log(event)
})
</script>

<template>
  <content-wrap style="height: calc(100vh - (35px + 50px + 2 * 20px + 5px))">
    <template #header>
      <router-link :to="{ name: 'UserCreate' }">
        <el-button type="success">Добавить</el-button>
      </router-link>
    </template>

    <el-table
      v-loading="loading"
      :data="users"
      border
      height="calc(100vh - (35px + 50px + 2 * 20px + 5px + 40px + 20px + 2 * 20px))"
    >
      <el-table-column prop="id" label="№" />
      <el-table-column prop="username" label="Имя пользователя" />
      <el-table-column prop="name" label="Имя" />
      <el-table-column prop="surname" label="Фамилия" />
      <el-table-column prop="patronymic" label="Отчество" />
      <el-table-column prop="roles" label="Роли" show-overflow-tooltip>
        <template #default="{ row: { roles } }">{{ roles }}</template>
      </el-table-column>
      <el-table-column prop="avatar" label="Аватар" />
    </el-table>
  </content-wrap>
</template>
