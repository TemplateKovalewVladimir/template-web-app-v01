<script setup lang="ts">
import { Ref, computed, onMounted, ref, unref } from 'vue'
import { FilterStringType, IFilterString, ColumnType } from '../types'

const props = defineProps<{ columnType: ColumnType | undefined }>()
const emit = defineEmits<{
  (e: 'createFilter', filter: IFilterString, closeMenu: boolean): void
}>()

const inputValue = ref<HTMLInputElement | null>(null)

const type: Ref<FilterStringType> = ref('contains')
const value = ref('')

const isTypeEmpty = computed(() => type.value === 'notnull' || type.value === 'null')

const createFilter = (closeMenu: boolean) => {
  const _value = unref(value).trim()

  if (_value) {
    emit('createFilter', { type: unref(type), value: _value }, closeMenu)
    value.value = ''
  }
  if (isTypeEmpty.value) emit('createFilter', { type: unref(type), value: '' }, closeMenu)
}

onMounted(() => {
  unref(inputValue)?.focus()
})
</script>

<template>
  <div class="flex flex-col w150px">
    <el-select v-model="type" class="mb5px" :teleported="false">
      <el-option-group>
        <el-option value="contains" label="Содержит" />
        <el-option value="notcontains" label="Не содержит" />
      </el-option-group>
      <template v-if="props.columnType === 'string'">
        <el-option-group>
          <el-option value="eq" label="Равно" />
          <el-option value="ne" label="Не равно" />
        </el-option-group>
        <el-option-group>
          <el-option value="null" label="Пусто" />
          <el-option value="notnull" label="Не пусто" />
        </el-option-group>
      </template>
    </el-select>
    <el-input
      v-if="!isTypeEmpty"
      ref="inputValue"
      v-model="value"
      class="mb5px"
      @keydown.enter.exact="createFilter(true)"
      @keydown.ctrl.enter.exact="createFilter(false)"
    />
    <el-button @click="createFilter(true)">Применить</el-button>
  </div>
</template>
