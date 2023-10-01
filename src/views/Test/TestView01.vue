<script setup lang="ts">
import { ContentWrap } from '@/components/ContentWrap'
import VirtualTable from './VirtualTable.vue'
</script>

<template>
  <content-wrap
    title="virtual-table"
    message="Таблица"
    style="height: calc(100vh - (35px + 50px + 2 * 20px + 5px))"
  >
    <virtual-table />
  </content-wrap>
</template>
