<script setup lang="ts">
import { useDesign } from '@/hooks/web/useDesign'
import { defineAsyncComponent, shallowRef, toRefs, watch } from 'vue'

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
const { icon } = toRefs(props)

const getIconComponent = () => {
  return defineAsyncComponent(
    // https://github.com/nuxt/nuxt/issues/15448#issuecomment-1397379989
    () => import(/* @vite-ignore */ `../../../assets/svgs/${props.icon}.svg?component`)
  )
}
let asyncIcon = shallowRef(getIconComponent())
watch(icon, () => {
  asyncIcon.value = getIconComponent()
})
</script>

<template>
  <el-icon :class="prefixCls" :size="size" :color="color"><component :is="asyncIcon" /></el-icon>
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
