<script setup lang="ts">
import { FormRules } from 'element-plus'
import { useRoute, useRouter } from 'vue-router'

import {
  UserCreateSchemaBackend,
  UserSchemaBackend,
  UserUpdateSchemaBackend
} from '@/api/generated'
import { createUser, deleteUser, getUser, updateUser } from '@/api/user'
import { ContentWrap } from '@/components/ContentWrap'
import { useCan } from '@/hooks/web/useCan'
import { simpleRules } from '@/utils/is'
import { getFullPathByName } from '@/utils/routerHelper'

import { userStatusKey } from './EventBusKey'
import { ActionType } from './types'
import { useActions } from './useActions'
import UserRoleChange from './UserRoleChange.vue'

const router = useRouter()
const route = useRoute()

const { isCan } = useCan()

const { action } = defineProps<{ action: ActionType }>()

const backRoute = getFullPathByName('UserTable', router.getRoutes())

const rulesUserCreate: FormRules<UserCreateSchemaBackend> = {
  username: [simpleRules.requiredBlur]
}

const initUser =
  action === 'create'
    ? {
        username: '',
        name: '',
        surname: '',
        patronymic: '',
        roles: {
          frontend: {}
        },
        avatar: ''
      }
    : Number.parseInt(route.params.userId as string)

const {
  dataForm: userForm,
  formRef,
  isCreate,
  isUpdate,
  isUpdateEmpty,
  create,
  update,
  remove,
  loading
} = useActions<UserSchemaBackend, UserCreateSchemaBackend, UserUpdateSchemaBackend>(
  action,
  initUser,
  userStatusKey,
  backRoute,
  getUser,
  createUser,
  updateUser,
  deleteUser
)
</script>

<template>
  <content-wrap v-loading="loading" style="height: calc(100vh - (35px + 50px + 2 * 20px + 5px))">
    <template #header>
      <el-button @click="router.push(backRoute)">Назад</el-button>

      <template v-if="isCreate">
        <el-button type="success" @click="create">Создать</el-button>
      </template>
      <template v-if="isUpdate">
        <el-button type="success" :disabled="isUpdateEmpty" @click="update">Изменить</el-button>
        <el-popconfirm width="300" title="Вы уверены, что хотите удалить это?" @confirm="remove">
          <template #reference>
            <el-button type="danger">Удалить</el-button>
          </template>
        </el-popconfirm>
      </template>
    </template>

    <el-form
      v-if="userForm"
      ref="formRef"
      :disabled="!isCan"
      :model="userForm"
      :rules="rulesUserCreate"
      label-width="150"
      label-position="left"
    >
      <el-row :gutter="40">
        <el-col :span="12">
          <el-divider style="margin-top: 0" content-position="left"
            >Информация о пользователе</el-divider
          >

          <el-form-item prop="username" label="Логин">
            <el-input v-model="userForm.username" placeholder="ivanov-i" />
          </el-form-item>
          <el-form-item prop="avatar" label="Аватарка">
            <el-input v-model="userForm.avatar" />
          </el-form-item>

          <el-divider content-position="left">
            <el-link type="primary">Запросить инфу из AD (ещё не реализовал)</el-link>
          </el-divider>

          <el-form-item prop="name" label="Имя">
            <el-input v-model="userForm.name" />
          </el-form-item>
          <el-form-item prop="surname" label="Фамилия">
            <el-input v-model="userForm.surname" />
          </el-form-item>
          <el-form-item prop="patronymic" label="Отчество">
            <el-input v-model="userForm.patronymic" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-divider style="margin-top: 0" content-position="left">Роли</el-divider>
          <user-role-change v-model="userForm.roles" />
        </el-col>
      </el-row>
    </el-form>
  </content-wrap>
</template>
