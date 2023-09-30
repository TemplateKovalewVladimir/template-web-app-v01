<script setup lang="ts">
import { ref } from 'vue'

const value1 = ref('')
</script>

<template>
  <h1>TestView02 {{ value1 }}</h1>
  <el-date-picker v-model="value1" type="date" />
</template>
