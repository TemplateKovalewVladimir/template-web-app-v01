<script setup lang="ts">
import { ComponentSize, ElDropdown, ElDropdownItem, ElDropdownMenu } from 'element-plus'
import { computed } from 'vue'

import { Icon } from '@/components/Icon'
import { useDesign } from '@/hooks/web/useDesign'
import { useAppStore } from '@/store/modules/app'

const { getPrefixCls } = useDesign()

const prefixCls = getPrefixCls('size-dropdown')

defineProps({
  color: { type: String, default: '' }
})

const SIZE = {
  small: 'Мини',
  default: 'Средний',
  large: 'Большой'
}

const appStore = useAppStore()

const sizeMap = computed(() => appStore.sizeMap)

const setCurrentSize = (size: ComponentSize) => {
  appStore.setCurrentSize(size)
}
</script>

<template>
  <ElDropdown :class="prefixCls" trigger="click" @command="setCurrentSize">
    <Icon :size="18" icon="mdi/format-size" :color="color" class="cursor-pointer" />
    <template #dropdown>
      <ElDropdownMenu>
        <ElDropdownItem v-for="item in sizeMap" :key="item" :command="item">
          {{ SIZE[item] }}
        </ElDropdownItem>
      </ElDropdownMenu>
    </template>
  </ElDropdown>
</template>
