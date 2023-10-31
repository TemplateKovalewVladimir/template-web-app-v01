<script setup lang="ts">
import { ContentWrap } from '@/components/ContentWrap'
import { Setting } from '@/layout/components/Setting'

import { useUserStore } from '@/store/modules/user'

const userStore = useUserStore()
</script>

<template>
  <el-row :gutter="20">
    <el-col :span="8">
      <content-wrap title="Настройки">
        <Setting />
      </content-wrap>
    </el-col>
    <el-col :span="16">
      <content-wrap title="Пользователь">
        <pre>{{ JSON.stringify(userStore.userInfo, null, 2) }}</pre>
      </content-wrap>
    </el-col>
  </el-row>
</template>
