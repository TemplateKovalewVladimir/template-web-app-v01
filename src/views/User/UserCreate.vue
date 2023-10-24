<script setup lang="ts">
import { ContentWrap } from '@/components/ContentWrap'
import { useEventBus } from '@vueuse/core'
import { useRouter } from 'vue-router'
import { userStatusKey } from './EventBusKey'
import { ref, Ref } from 'vue'
import { UserCreateSchemaBackend } from '@/api/generated'
import { asyncRouterMap } from '@/router'
import { convertToRoleType, RoleType, convertToUserRolesSchema } from './utils'
import { createUser } from '@/api/user'
import { FormInstance, FormRules } from 'element-plus'
import { Message } from '@/utils/message'
import { validateForm, simpleRules } from '@/utils/is'

const router = useRouter()
const busUserStatus = useEventBus(userStatusKey)

const roles: Ref<RoleType[]> = ref(convertToRoleType(asyncRouterMap))

const formUserCreate = ref<UserCreateSchemaBackend>({
  username: '',
  name: '',
  surname: '',
  patronymic: '',
  roles: {
    frontend: {}
  },
  avatar: ''
})

const formRef = ref<FormInstance>()

const rulesUserCreate = ref<FormRules<UserCreateSchemaBackend>>({
  username: [simpleRules.requiredBlur]
})

const save = async () => {
  const { isValid } = await validateForm(formRef.value)
  if (!isValid) {
    Message('Ошибка', 'Ошибка валидации', 'error')
    return
  }
  formUserCreate.value.roles = convertToUserRolesSchema(roles.value)
  const { data } = await createUser(formUserCreate.value)
  console.log(data)
  busUserStatus.emit({ status: 'create' })
  router.push({ name: 'UserTable' })
}
</script>

<template>
  <content-wrap style="height: calc(100vh - (35px + 50px + 2 * 20px + 5px))">
    <template #header>
      <el-button @click="router.go(-1)">Назад</el-button>
      <el-button type="success" @click="save">Создать</el-button>
    </template>

    <el-form
      ref="formRef"
      :model="formUserCreate"
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
            <el-input v-model="formUserCreate.username" placeholder="ivanov-i" />
          </el-form-item>
          <el-form-item prop="avatar" label="Аватарка">
            <el-input v-model="formUserCreate.avatar" />
          </el-form-item>

          <el-divider content-position="left">
            <el-link type="primary">Запросить инфу из AD</el-link>
          </el-divider>

          <el-form-item prop="name" label="Имя">
            <el-input v-model="formUserCreate.name" />
          </el-form-item>
          <el-form-item prop="surname" label="Фамилия">
            <el-input v-model="formUserCreate.surname" />
          </el-form-item>
          <el-form-item prop="patronymic" label="Отчество">
            <el-input v-model="formUserCreate.surname" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-divider style="margin-top: 0" content-position="left">Роли </el-divider>

          <el-table
            :data="roles"
            row-key="name"
            border
            default-expand-all
            height="calc(100vh - (35px + 50px + 2 * 20px + 5px + 2 * 60px))"
          >
            <el-table-column prop="name" label="name" sortable />
            <el-table-column prop="title" label="title" />
            <el-table-column label="role" width="150">
              <template #default="{ row }">
                <el-select v-if="!row.children" v-model="row.role">
                  <el-option value="NONE" label="Нет доступа" />
                  <el-option value="RO" label="Просмотр" />
                  <el-option value="RW" label="Редактирование" />
                </el-select>
              </template>
            </el-table-column>
          </el-table>
        </el-col>
      </el-row>
    </el-form>
  </content-wrap>
</template>
