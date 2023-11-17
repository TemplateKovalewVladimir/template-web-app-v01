import type { EventBusKey } from '@vueuse/core'

export type ActionType = 'create' | 'update'

export type EventBusActionKeyType = EventBusKey<{
  status: 'create' | 'update' | 'delete'
}>
