<script setup lang="ts">
import { computed, Ref, ref, unref } from 'vue'

import { dateToBackendFormat, getCapitalizedMonth } from '@/utils/date'

import { FilterStringType, IFilterDate } from '../types'
import { FILTER_TYPE_LABEL } from '../types/constants'

const currentDate = new Date()
const currentMouth = currentDate.getMonth()
const currentYear = currentDate.getFullYear()

const emit = defineEmits<{
  (e: 'createFilter', filter: IFilterDate, closeMenu: boolean): void
}>()

const type = ref('eq')
const value = ref('')
const valueRange: Ref<string | [string, string]> = ref('')

const isValueRange = computed(() => {
  if (['eq', 'before', 'after'].includes(type.value)) return false
  return true
})

const changeType = () => {
  value.value = ''
  valueRange.value = ''

  if (typeof type.value === 'number') {
    const start = new Date(currentYear, type.value, 1)
    const end = new Date(currentYear, type.value + 1, 0)
    valueRange.value = [dateToBackendFormat(start), dateToBackendFormat(end)]
  }
}

const createFilter = (closeMenu: boolean) => {
  const _value = isValueRange.value ? unref(valueRange) : unref(value)
  const _type = (isValueRange.value ? 'between' : unref(type)) as FilterStringType

  if (_value) {
    emit('createFilter', { type: _type, value: _value }, closeMenu)
    value.value = ''
    valueRange.value = ''
  }
}
</script>

<template>
  <div class="flex flex-col w210px">
    <el-select v-model="type" class="mb5px" :teleported="false" @change="changeType">
      <el-option-group>
        <el-option value="eq" :label="FILTER_TYPE_LABEL.eq" />
      </el-option-group>
      <el-option-group>
        <el-option value="before" :label="FILTER_TYPE_LABEL.before" />
        <el-option value="after" :label="FILTER_TYPE_LABEL.after" />
        <el-option value="between" :label="FILTER_TYPE_LABEL.between" />
      </el-option-group>
      <el-option-group>
        <el-option
          v-for="month in 6"
          :key="month"
          :value="currentMouth - month + 1"
          :label="getCapitalizedMonth(currentMouth - month + 1 + 1)"
        />
      </el-option-group>
    </el-select>

    <el-date-picker
      v-if="isValueRange"
      v-model="valueRange"
      style="width: 190px"
      format="DD-MM-YYYY"
      value-format="YYYY-MM-DD"
      class="mb5px"
      type="daterange"
      :teleported="false"
    />
    <el-date-picker
      v-else
      v-model="value"
      style="width: 100%"
      format="DD-MM-YYYY"
      value-format="YYYY-MM-DD"
      class="mb5px"
      type="date"
      :teleported="false"
    />

    <el-button @click="createFilter(true)">Применить</el-button>
  </div>
</template>
