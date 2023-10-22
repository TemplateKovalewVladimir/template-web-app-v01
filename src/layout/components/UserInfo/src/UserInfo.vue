<script setup lang="ts">
import { ElDropdown, ElDropdownMenu, ElDropdownItem } from 'element-plus'
import { useI18n } from '@/hooks/web/useI18n'
import { useStorage } from '@/hooks/web/useStorage'
import { resetRouter } from '@/router'
import { useRouter } from 'vue-router'
import { useDesign } from '@/hooks/web/useDesign'
import { useTagsViewStore } from '@/store/modules/tagsView'
import { useUserStore } from '@/store/modules/user'
import defaultAvatarSrc from '@/assets/imgs/default_rabbit.gif'
import { usePermissionStore } from '@/store/modules/permission'

const tagsViewStore = useTagsViewStore()
const permissionStore = usePermissionStore()
const userStore = useUserStore()

const { getPrefixCls } = useDesign()
const prefixCls = getPrefixCls('user-info')

const { t } = useI18n()

const { clear } = useStorage()

const { replace } = useRouter()

const username = userStore.userInfo?.username
// const avatar = userStore.userInfo?.avatar
// const avatarSrc = avatar ? avatar : defaultAvatarSrc

const loginOut = () => {
  clear()
  userStore.$reset()
  permissionStore.$reset()
  tagsViewStore.delAllViews()
  resetRouter()
  replace('/login')
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
          <div>{{ t('common.profile') }}</div>
        </ElDropdownItem>
        <ElDropdownItem divided>
          <div @click="loginOut">{{ t('common.loginOut') }}</div>
        </ElDropdownItem>
      </ElDropdownMenu>
    </template>
  </ElDropdown>
</template>
