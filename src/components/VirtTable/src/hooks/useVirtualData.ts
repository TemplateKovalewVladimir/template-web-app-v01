import { loadingWrapper } from '@/utils/loading'
import { useVirtualList, useInfiniteScroll } from '@vueuse/core'
import { Ref, onMounted, ref, unref } from 'vue'
import { Columns, onLoadDataType } from '../types'

const resetScroll = (container: Ref<HTMLElement | null>) => {
  const virtualList = unref(container)
  if (virtualList) virtualList.scrollTo(0, 0)
}

export const useVirtualData = (
  onLoadData: onLoadDataType,
  columns: Columns,
  sizePage: number,
  rowHeight: number,
  virtualListOverscan: number,
  infiniteScrollDistance: number
) => {
  const loading = ref(false)

  const data: Ref<any> = ref([])
  const currentPage = ref(0)

  onMounted(async () => {
    await getData()
  })

  // Загрузка/Обновление данных
  const getData = loadingWrapper(loading, async (options = { reload: false }) => {
    const sort = columns.getSort()
    const filters = columns.getFilters()
    currentPage.value = options.reload ? 1 : currentPage.value + 1

    const newData = await onLoadData({ page: currentPage.value, size: sizePage, sort, filters })

    if (options.reload) {
      resetScroll(virtualContainerProps.ref)
      data.value = newData
    } else {
      data.value.push(...newData)
    }
  })
  const reloadData = async () => {
    await getData({ reload: true })
  }

  // Виртуальный список
  const {
    list: virtualData,
    containerProps: virtualContainerProps,
    wrapperProps: virtualWrapperProps
  } = useVirtualList(data, {
    itemHeight: rowHeight,
    overscan: virtualListOverscan
  })

  // Загрузка новых данных при scroll`е
  useInfiniteScroll(
    virtualContainerProps.ref,
    async () => {
      await getData()
    },
    { distance: infiniteScrollDistance }
  )

  return {
    loading,
    data,
    reloadData,
    currentPage,
    virtualData,
    virtualContainerProps,
    virtualWrapperProps
  }
}
