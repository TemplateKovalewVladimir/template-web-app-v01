<script setup lang="ts">
import { reactive } from 'vue'

defineProps({
  msg: String
})

interface User {
  id: number
}

const user: User = reactive({
  id: 1
})

const testClk = (evt: Event) => {
  console.log(evt.target)
  user.id++
}
</script>

<template>
  <h1>{{ msg }}</h1>

  <p>{{ user }}</p>
  <button @click="testClk">test</button>
</template>
