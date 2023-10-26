<script setup lang="ts">
import { ContentWrap } from '@/components/ContentWrap'
import { useEventBus } from '@vueuse/core'
import { useRouter, useRoute } from 'vue-router'
import { ref, Ref, computed, onMounted, watch } from 'vue'
import {
  UserCreateSchemaBackend,
  UserSchemaBackend,
  UserUpdateSchemaBackend
} from '@/api/generated'
import { createUser, deleteUser, getUser, updateUser } from '@/api/user'
import { FormInstance, FormRules } from 'element-plus'
import { Message } from '@/utils/message'
import { validateForm, simpleRules } from '@/utils/is'
import { loadingWrapper } from '@/utils/loading'
import { userStatusKey } from './EventBusKey'
import UserRoleChange from './UserRoleChange.vue'
import { cloneDeep, isEqual } from 'lodash-es'

const { controlType } = defineProps<{
  controlType: 'create' | 'update'
}>()

const isCreate = computed(() => controlType === 'create')
const isUpdate = computed(() => controlType === 'update')
const isUserUpdateEmpty = computed(() => Object.keys(userUpdate.value).length === 0)

const router = useRouter()
const route = useRoute()
const busUserStatus = useEventBus(userStatusKey)

const backRoute = { name: 'UserTable' }

let userForm: Ref<UserSchemaBackend | UserCreateSchemaBackend>
let userInitial: Ref<UserSchemaBackend | UserCreateSchemaBackend>
let userUpdate: Ref<UserUpdateSchemaBackend> = ref({})

const formRef = ref<FormInstance>()
const rulesUserCreate: FormRules<UserCreateSchemaBackend> = {
  username: [simpleRules.requiredBlur]
}

const loading = ref<boolean>(false)

function getObjectDifference(obj1: any, obj2: any): any {
  const diffObj: any = {}

  for (const key in obj1) {
    if (!obj2.hasOwnProperty(key)) {
      diffObj[key] = null
    }
  }

  for (const key in obj2) {
    if (!obj1.hasOwnProperty(key)) {
      diffObj[key] = obj2[key]
    } else {
      if (!isEqual(obj1[key], obj2[key])) diffObj[key] = obj2[key]
    }
  }

  return diffObj
}

function cloneUser(user) {
  if (userInitial) userInitial.value = cloneDeep(user)
  else userInitial = ref(cloneDeep(user))
  if (userForm) userForm.value = user
  else userForm = ref(user)
}

onMounted(
  loadingWrapper(loading, async () => {
    if (isCreate.value) {
      userForm = ref({
        username: '',
        name: '',
        surname: '',
        patronymic: '',
        roles: {
          frontend: {}
        },
        avatar: ''
      })
    }
    if (isUpdate.value) {
      const userId = Number.parseInt(route.params.userId as string)
      const { data } = await getUser(userId)
      cloneUser(data)

      watch(
        userForm,
        () => {
          userUpdate.value = getObjectDifference(userInitial.value, userForm.value)
        },
        { deep: true }
      )
    }
  })
)

const save = loadingWrapper(loading, async () => {
  const { isValid } = await validateForm(formRef.value)
  if (!isValid) throw Error('Ошибка валидации')

  const { data } = await createUser(userForm.value)
  Message('Успешно', `Пользователь создан ${data.id}`)
  busUserStatus.emit({ status: 'create' })
  router.push(backRoute)
})

const update = loadingWrapper(loading, async () => {
  const { isValid } = await validateForm(formRef.value)
  if (!isValid) throw Error('Ошибка валидации')

  const user = userForm.value as UserSchemaBackend
  const { data } = await updateUser(user.id, userUpdate.value)
  Message('Успешно', `Пользователь изменен ${data.id}`)
  cloneUser(data)
})

const remove = loadingWrapper(loading, async () => {
  const user = userForm.value as UserSchemaBackend
  const { data } = await deleteUser(user.id)
  Message('Успешно', `Пользователь удален ${data.id}`)
  busUserStatus.emit({ status: 'delete' })
  router.push(backRoute)
})
</script>

<template>
  <content-wrap v-loading="loading" style="height: calc(100vh - (35px + 50px + 2 * 20px + 5px))">
    <template #header>
      <el-button @click="router.push(backRoute)">Назад</el-button>

      <template v-if="isCreate">
        <el-button type="success" @click="save">Создать</el-button>
      </template>
      <template v-if="isUpdate">
        <el-button type="success" :disabled="isUserUpdateEmpty" @click="update">Изменить</el-button>
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
            <el-link type="primary">Запросить инфу из AD</el-link>
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

          <pre>{{ userUpdate }}</pre>
        </el-col>
        <el-col :span="12">
          <el-divider style="margin-top: 0" content-position="left">Роли</el-divider>
          <user-role-change v-model="userForm.roles" />
        </el-col>
      </el-row>
    </el-form>
  </content-wrap>
</template>
