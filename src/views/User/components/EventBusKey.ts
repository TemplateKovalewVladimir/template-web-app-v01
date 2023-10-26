import type { EventBusKey } from '@vueuse/core'

export const userStatusKey: EventBusKey<{ status: 'create' | 'update' | 'delete' }> =
  Symbol('userStatusKey')
