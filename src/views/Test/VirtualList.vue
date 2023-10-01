<script setup lang="ts">
import { useVirtualList, useInfiniteScroll } from '@vueuse/core'
import { ref } from 'vue'

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms))
}

const allItems = ref(Array.from(Array(100).keys()).map((i) => i))

const { list, containerProps, wrapperProps } = useVirtualList(allItems, {
  itemHeight: 28 + 4,
  overscan: 10
})

useInfiniteScroll(
  containerProps.ref,
  async () => {
    await sleep(1000)
    allItems.value.push(...Array.from(Array(60).keys()).map((i) => i))
  },
  { distance: 10 }
)
</script>

<template>
  <h2>length: {{ allItems.length }}</h2>
  <div class="h-150px">
    <div>{{ containerProps }}</div>
    <div>{{ wrapperProps }}</div>
    <!-- <div >{{ list }}</div> -->
  </div>

  <div v-bind="containerProps" class="h-600px">
    <div v-bind="wrapperProps">
      <div v-for="{ index, data } in list" :key="index" class="h-28px bg-red-2 mb-4px">
        Row {{ index }} <span>({{ data }})</span>
      </div>
    </div>
  </div>
</template>
