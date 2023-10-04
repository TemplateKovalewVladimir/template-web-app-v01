import VirtTable from '../VirtTable.vue'

export type TypeVirtTable = InstanceType<typeof VirtTable> | null

export interface Column {
  prop: string
  label: string
  width: number
  showOverflowTooltip?: boolean
}
