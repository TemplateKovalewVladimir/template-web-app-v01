import { ref, watch } from 'vue'

import { useAppStoreWithOut } from '@/store/modules/app'
import { isString } from '@/utils/is'

const appStore = useAppStoreWithOut()

export const useTitle = (newTitle?: string) => {
  const title = ref(newTitle ? `${appStore.getTitle} - ${newTitle}` : appStore.getTitle)

  watch(
    title,
    (n, o) => {
      if (isString(n) && n !== o && document) {
        document.title = n
      }
    },
    { immediate: true }
  )

  return title
}
