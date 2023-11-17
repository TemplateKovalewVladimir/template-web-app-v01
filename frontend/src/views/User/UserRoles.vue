<script setup lang="ts">
import { ContentWrap } from '@/components/ContentWrap'
import { asyncRouterMap } from '@/router'
</script>

<template>
  <el-row :gutter="10" style="height: calc(100vh - (35px + 50px + 2 * 20px + 5px))">
    <el-col :span="12">
      <content-wrap class="h-full">
        <el-table
          :data="asyncRouterMap"
          row-key="name"
          border
          default-expand-all
          height="calc(100vh - (35px + 50px + 2 * 20px + 5px + 2 * 20px))"
        >
          <el-table-column prop="name" label="name" sortable />
          <el-table-column prop="meta.title" label="title" />
        </el-table>
      </content-wrap>
    </el-col>
    <el-col :span="12">
      <content-wrap class="h-full">
        <el-scrollbar height="calc(100vh - (35px + 50px + 2 * 20px + 5px + 2 * 20px))">
          <pre class="m0">{{ asyncRouterMap }}</pre>
        </el-scrollbar>
      </content-wrap>
    </el-col>
  </el-row>
</template>
