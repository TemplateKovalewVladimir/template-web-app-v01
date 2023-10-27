<script setup lang="ts">
import { UserRolesSchemaBackend } from '@/api/generated'
import { asyncRouterMap } from '@/router'
import { RoleType, convertToRoleType, convertToUserRolesSchema } from './utils'
import { ref, Ref, watch } from 'vue'
import { isEqual } from 'lodash-es'

const userRoles = defineModel<UserRolesSchemaBackend>({ required: true })

const roles: Ref<RoleType[]> = ref(convertToRoleType(asyncRouterMap, userRoles.value))

watch(
  userRoles,
  () => {
    const convert = convertToRoleType(asyncRouterMap, userRoles.value)
    if (isEqual(convert, roles.value)) return

    roles.value = convertToRoleType(asyncRouterMap, userRoles.value)
  },
  { deep: true }
)

watch(
  roles,
  () => {
    const convert = convertToUserRolesSchema(roles.value)
    if (isEqual(convert, userRoles.value)) return

    userRoles.value = convert
  },
  { deep: true }
)
</script>

<template>
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
        <el-select v-model="row.role">
          <el-option value="NONE" label="Нет доступа" />
          <el-option value="RO" label="Просмотр" />
          <el-option value="RW" label="Редактирование" />
        </el-select>
      </template>
    </el-table-column>
  </el-table>
</template>
