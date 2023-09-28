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
  <router-link
    v-for="(router, i) in constantRouterMap"
    :key="i"
    :to="{ name: router.name }"
    class="mr-5"
    >{{ router.name }}
  </router-link>

  <router-view />
</template>
