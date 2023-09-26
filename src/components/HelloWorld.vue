<script setup lang="ts">
import { reactive } from 'vue'
import { useUserStore } from '@/store/user'

defineProps({
  msg: String
})

const userStore = useUserStore()

interface User {
  id: number
}

const user: User = reactive({
  id: 1
})

const testClk = (evt: Event) => {
  console.log(evt.target)
  console.log(user)
  user.id1 = 12
  user.id++
}

const storeTestClk = () => {
  userStore.role.push('123')
}
</script>

<template>
  <h1>{{ msg }}</h1>

  <p>{{ user }}</p>
  <button @click="testClk">test</button>

  <br />
  <br />
  <div>{{ userStore }}</div>
  <button @click="storeTestClk">store test</button>
</template>
