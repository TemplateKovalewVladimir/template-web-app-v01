<script setup lang="ts">
import { Icon } from '@/components/Icon'
import { useSlots } from 'vue'

defineProps({
  title: { type: String, default: '' },
  message: { type: String, default: '' }
})

const slots = useSlots()
</script>

<template>
  <ElCard shadow="never">
    <template v-if="title || slots.hasOwnProperty('header')" #header>
      <slot name="header">
        <div class="flex items-center">
          <span class="text-16px font-700">{{ title }}</span>
          <ElTooltip v-if="message" effect="dark" placement="right">
            <template #content>
              <div class="max-w-200px">{{ message }}</div>
            </template>
            <Icon class="ml-5px" icon="bi/question-circle-fill" :size="14" />
          </ElTooltip>
          <div class="flex pl-20px flex-grow">
            <slot name="header-after-message"></slot>
          </div>
        </div>
      </slot>
    </template>
    <div>
      <slot></slot>
    </div>
  </ElCard>
</template>
