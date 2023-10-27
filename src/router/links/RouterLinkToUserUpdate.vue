<script setup lang="ts">
const { userId } = defineProps<{ userId: number }>()
</script>

<template>
  <router-link :to="'/setting/user/' + userId"
    ><slot
      ><el-link type="primary" style="font-size: 12px">{{ userId }}</el-link></slot
    ></router-link
  >
</template>
