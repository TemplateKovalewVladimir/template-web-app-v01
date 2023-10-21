<script setup lang="ts">
import { HTTPBasicCredentials } from '@/api/generated'
import { getTokenBasic, getTokenSSO } from '@/api/login'
import { ContentWrap } from '@/components/ContentWrap'
import { useDesign } from '@/hooks/web/useDesign'
import { ThemeSwitch } from '@/layout/components/ThemeSwitch'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/store/modules/user'
import { ref } from 'vue'

defineOptions({
  // eslint-disable-next-line vue/multi-word-component-names
  name: 'Login'
})

const { getPrefixCls } = useDesign()
const prefixCls = getPrefixCls('login')

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const isSSO = ref(true)
const creds = ref<HTTPBasicCredentials>({
  username: '',
  password: ''
})

const routerPush = () => {
  const redirect = route.query?.redirect
  router.push(typeof redirect === 'string' ? redirect : '/')
}

const loginBasic = async () => {
  const { data } = await getTokenBasic(creds.value)
  userStore.token = data.token

  routerPush()
}

const loginSSO = async () => {
  try {
    const { data } = await getTokenSSO()
    userStore.token = data.token

    routerPush()
  } catch {
    isSSO.value = false
  }
}
</script>

<template>
  <div :class="prefixCls" class="h-full w-full flex flex-items-center flex-justify-center">
    <content-wrap title="Тестовая программа" message="Нажмите на кнопку войти" class="w-400px">
      <template #header>
        <ThemeSwitch class="w-full flex flex-justify-end" />
      </template>

      <template v-if="isSSO">
        <el-button type="primary" size="large" class="w-100%" @click="loginSSO"
          >Войти без пароля</el-button
        >
        <div class="h-10px"></div>
        <el-button class="w-100%" @click="isSSO = false">Войти с паролем</el-button>
      </template>

      <transition name="el-zoom-in-center">
        <el-form v-if="!isSSO" :model="creds" label-position="top" size="large">
          <el-form-item label="Имя пользователя">
            <el-input v-model="creds.username" clearable placeholder="ivanov-i" />
          </el-form-item>
          <el-form-item label="Пароль">
            <el-input
              v-model="creds.password"
              show-password
              clearable
              type="password"
              @keyup.enter="loginBasic"
            />
          </el-form-item>
          <el-button type="primary" class="w-100%" @click="loginBasic">Войти</el-button>
        </el-form>
      </transition>
    </content-wrap>
  </div>
</template>

<style lang="less" scoped>
@prefix-cls: ~'@{namespace}-login';

.@{prefix-cls} {
  background-color: var(--app-content-bg-color);
}
</style>
