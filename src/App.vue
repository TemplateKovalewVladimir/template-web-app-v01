<script setup lang="ts">
import { Ref, ref } from 'vue'
import HelloWorld from '@/components/HelloWorld.vue'
import TestDefineModel from '@/components/TestDefineModel.vue'
import { constantRouterMap } from '@/router'

const testInput01: Ref<string> = ref('')
const testInput02: Ref<string> = ref('')
</script>

<template>
  <HelloWorld msg="Test 123" />
  <hr />

  <TestDefineModel v-model="testInput01" />
  <TestDefineModel v-model="testInput02" />
  <el-button @click="testInput02 = '123'">testInput02 = 123</el-button>

  <hr />
  <hr />

  <router-link class="mr-5" v-for="route in constantRouterMap" :to="{name: route.name}">{{ route.name }}</router-link>

  <router-view />
</template>
