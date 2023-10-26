<script setup lang="ts">
import { UserSchemaBackend } from '@/api/generated'
import { getUsers } from '@/api/user'
import { ContentWrap } from '@/components/ContentWrap'
import { onMounted, ref } from 'vue'
import { userStatusKey } from './components/EventBusKey'
import { useEventBus } from '@vueuse/core'
import { loadingWrapper } from '@/utils/loading'
import { useRouter } from 'vue-router'

const router = useRouter()

const users = ref<UserSchemaBackend[]>([])
const loading = ref(false)

const loadData = loadingWrapper(loading, async () => {
  const { data } = await getUsers()
  users.value = data
})

onMounted(async () => {
  await loadData()
})

const busUserStatus = useEventBus(userStatusKey)
busUserStatus.on(async (event) => {
  console.log(event.status)
  await loadData()
})
</script>

<template>
  <content-wrap style="height: calc(100vh - (35px + 50px + 2 * 20px + 5px))">
    <template #header>
      <router-link :to="{ name: 'UserCreate' }">
        <el-button type="success">Добавить</el-button>
      </router-link>
      <el-button class="ml-3" type="primary" @click="loadData">Обновить таблицу</el-button>
    </template>

    <el-table
      v-loading="loading"
      :data="users"
      border
      height="calc(100vh - (35px + 50px + 2 * 20px + 5px + 40px + 20px + 2 * 20px))"
    >
      <el-table-column prop="id" label="№" width="60">
        <template #default="{ row }"
          ><el-link
            type="primary"
            style="font-size: 12px"
            @click="router.push({ name: 'UserUpdate', params: { userId: row.id } })"
            >{{ row.id }}</el-link
          ></template
        >
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
