import { Ref } from 'vue'

import { Message } from '@/utils/message'

export function loadingWrapper(loading: Ref<boolean>, cb: (...args: any) => Promise<void>) {
  return async (...args: any) => {
    loading.value = true

    try {
      await cb(...args)
      loading.value = false
    } catch (e: any) {
      Message('Ошибка', e?.message as string, 'error')
    }
  }
}
