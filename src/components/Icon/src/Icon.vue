<script setup lang="ts">
import { computed, unref } from 'vue'
import { ElIcon } from 'element-plus'
import { useDesign } from '@/hooks/web/useDesign'
import { Icon } from '@iconify/vue'

const { getPrefixCls } = useDesign()

defineOptions({
  // eslint-disable-next-line vue/multi-word-component-names
  name: 'Icon'
})

const prefixCls = getPrefixCls('icon')

const props = defineProps({
  icon: { type: String, required: true },
  color: { type: String, default: null },
  size: { type: Number, default: 16 },
  hoverColor: { type: String, default: null }
})

const isLocal = computed(() => props.icon.startsWith('svg-icon:'))

const symbolId = computed(() => {
  return unref(isLocal) ? `#icon-${props.icon.split('svg-icon:')[1]}` : props.icon
})

const getIconifyStyle = computed(() => {
  const { color, size } = props
  return {
    fontSize: `${size}px`,
    color
  }
})
</script>

<template>
  <ElIcon :class="prefixCls" :size="size" :color="color">
    <svg v-if="isLocal" aria-hidden="true">
      <use :xlink:href="symbolId" />
    </svg>

    <Icon v-else :icon="icon" :style="getIconifyStyle" />
  </ElIcon>
</template>

<style lang="less" scoped>
@prefix-cls: ~'@{namespace}-icon';

.@{prefix-cls},
.iconify {
  &:hover {
    :deep(svg) {
      // stylelint-disable-next-line
      color: v-bind(hoverColor) !important;
    }
  }
}
</style>
