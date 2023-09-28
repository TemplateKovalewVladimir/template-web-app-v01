<script setup lang="ts">
import { ref } from 'vue'

const text = ref('')
</script>

<template>
  <div class="p-20">
    <el-input v-model="text" />
  </div>
</template>
