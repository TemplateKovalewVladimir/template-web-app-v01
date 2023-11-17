<script setup lang="ts">
import { computed } from 'vue'

import { useDesign } from '@/hooks/web/useDesign'

const { getPrefixCls } = useDesign()
const prefixCls = getPrefixCls('icon')

defineOptions({
  // eslint-disable-next-line vue/multi-word-component-names
  name: 'Icon'
})

const props = defineProps({
  icon: { type: String, required: true },
  color: { type: String, default: null },
  size: { type: Number, default: 16 },
  hoverColor: { type: String, default: null }
})

const symbolId = computed(() => `#icon-${props.icon}`)
</script>

<template>
  <el-icon :class="prefixCls" :size="size" :color="color">
    <svg aria-hidden="true">
      <use :href="symbolId" />
    </svg>
  </el-icon>
</template>

<style lang="less" scoped>
@prefix-cls: ~'@{namespace}-icon';

.@{prefix-cls} {
  &:hover {
    :deep(svg) {
      // stylelint-disable-next-line
      color: v-bind(hoverColor) !important;
    }
  }
}
</style>
