<script setup lang="ts">
const modelValue = defineModel<string>({ required: true })

const test = () => {
  console.log(modelValue.value)
}
</script>

<template>
  <div class="b-solid b-5 b-red m-b-1 py-2">
    <input v-model="modelValue" />
    <button @click="test">modelValue to log</button>
  </div>
</template>
