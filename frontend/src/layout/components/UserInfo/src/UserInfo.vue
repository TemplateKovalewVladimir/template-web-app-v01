<script setup lang="ts">
import { ElDropdown, ElDropdownItem, ElDropdownMenu } from 'element-plus'
import { useRouter } from 'vue-router'

import defaultAvatarSrc from '@/assets/imgs/default_rabbit.gif'
import { useDesign } from '@/hooks/web/useDesign'
import { useStorage } from '@/hooks/web/useStorage'
import { resetRouter } from '@/router'
import { usePermissionStore } from '@/store/modules/permission'
import { useTagsViewStore } from '@/store/modules/tagsView'
import { useUserStore } from '@/store/modules/user'

const tagsViewStore = useTagsViewStore()
const permissionStore = usePermissionStore()
const userStore = useUserStore()

const { getPrefixCls } = useDesign()
const prefixCls = getPrefixCls('user-info')

const { clear } = useStorage()

const router = useRouter()

const username = userStore.userInfo?.username
// const avatar = userStore.userInfo?.avatar
// const avatarSrc = avatar ? avatar : defaultAvatarSrc

const loginOut = () => {
  clear()
  userStore.$reset()
  permissionStore.$reset()
  tagsViewStore.delAllViews()
  resetRouter()
  router.replace('/login')
}
const userSettings = () => {
  router.push('/setting/profile')
}
</script>

<template>
  <ElDropdown class="custom-hover" :class="prefixCls" trigger="click">
    <div class="flex items-center">
      <img :src="defaultAvatarSrc" class="w-[calc(var(--logo-height)-10px)] rounded-[50%]" />
      <span class="<lg:hidden text-14px pl-[5px] text-[var(--top-header-text-color)]">{{
        username
      }}</span>
    </div>
    <template #dropdown>
      <ElDropdownMenu>
        <ElDropdownItem>
          <div @click="userSettings">Профиль</div>
        </ElDropdownItem>
        <ElDropdownItem divided>
          <div @click="loginOut">Выйти</div>
        </ElDropdownItem>
      </ElDropdownMenu>
    </template>
  </ElDropdown>
</template>
