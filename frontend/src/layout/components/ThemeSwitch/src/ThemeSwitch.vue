<script setup lang="ts">
import { ElSwitch } from 'element-plus'
import { ref } from 'vue'

import { useDesign } from '@/hooks/web/useDesign'
import { useIcon } from '@/hooks/web/useIcon'
import { useAppStore } from '@/store/modules/app'

const { getPrefixCls } = useDesign()

const prefixCls = getPrefixCls('theme-switch')

const Sun = useIcon({ icon: 'emojione-monotone/sun', color: '#fde047' })

const CrescentMoon = useIcon({ icon: 'emojione-monotone/crescent-moon', color: '#fde047' })

const appStore = useAppStore()

// 初始化获取是否是暗黑主题
const isDark = ref(appStore.getIsDark)

// 设置switch的背景颜色
const blackColor = 'var(--el-color-black)'

const themeChange = (val: boolean) => {
  appStore.setIsDark(val)
}
</script>

<template>
  <ElSwitch
    v-model="isDark"
    :class="prefixCls"
    inline-prompt
    :border-color="blackColor"
    :inactive-color="blackColor"
    :active-color="blackColor"
    :active-icon="Sun"
    :inactive-icon="CrescentMoon"
    @change="themeChange"
  />
</template>

<style lang="less" scoped>
:deep(.el-switch__core .el-switch__inner .is-icon) {
  overflow: visible;
}
</style>
