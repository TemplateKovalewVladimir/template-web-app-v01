import { VirtTableType } from '../types'

export const useRestoreScrollPositionInTable = (refNames: string[]) => ({
  beforeRouteEnter(_to, _from, next) {
    next((vm) => {
      for (const refNameTable of refNames) {
        const table = vm.$refs[refNameTable] as VirtTableType
        table?.restoreScrollPosition()
      }
    })
  },
  beforeRouteLeave() {
    for (const refNameTable of refNames) {
      const vm = this as any
      const table = vm.$refs[refNameTable] as VirtTableType
      table?.saveScrollPosition()
    }
  }
})
