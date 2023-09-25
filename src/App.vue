<script setup lang="ts">
import { Ref, ref } from 'vue'
import HelloWorld from './components/HelloWorld.vue'
import TestDefineModel from './components/TestDefineModel.vue'

const testInput01: Ref<string> = ref('')
const testInput02: Ref<string> = ref('')
</script>

<template>
  <HelloWorld msg="Test 123" />
  <hr />

  <TestDefineModel v-model="testInput01" />
  <TestDefineModel v-model="testInput02" />
  <button @click="testInput02 = '123'">testInput02 = 123</button>

  <hr />
</template>
