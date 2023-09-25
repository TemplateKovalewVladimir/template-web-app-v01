<script setup lang="ts">
const modelValue = defineModel<string>({ required: true })

const test = () => {
  console.log(modelValue.value)
}
</script>

<template>
  <div style="border: 1px solid red">
    <input v-model="modelValue" />
    <button @click="test">modelValue to log</button>
  </div>
</template>
