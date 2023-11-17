import { useInfiniteScroll, useVirtualList } from '@vueuse/core'
import { onMounted, Ref, ref, unref } from 'vue'

import { loadingWrapper } from '@/utils/loading'

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
  const isAllDataLoaded = ref(false)

  const data: Ref<any> = ref([])
  const currentPage = ref(0)

  onMounted(async () => {
    await getData()
  })

  // Загрузка/Обновление данных
  const getData = loadingWrapper(loading, async (options = { reload: false }) => {
    if (isAllDataLoaded.value) return

    const sort = columns.getSort()
    const filters = columns.getFilters()
    currentPage.value = options.reload ? 1 : currentPage.value + 1

    const newData = await onLoadData({ page: currentPage.value, size: sizePage, sort, filters })

    if (newData.length < sizePage) isAllDataLoaded.value = true

    for (const column of columns)
      if (column.formatter)
        for (const v of newData) v[`_${column.prop}`] = column.formatter(v[column.prop])

    if (options.reload) {
      resetScroll(virtualContainerProps.ref)
      data.value = newData
    } else {
      data.value.push(...newData)
    }

    // Bugfix: не отображаются данные, если они все помещаются в контейнер без scroll`а.
    // Что бы они отобразились нужно принудительно сделать перерендер
    if (currentPage.value === 1) scrollTo(0)
  })
  const reloadData = async () => {
    isAllDataLoaded.value = false
    await getData({ reload: true })
  }

  // Виртуальный список
  const {
    list: virtualData,
    scrollTo,
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
    isAllDataLoaded,
    data,
    reloadData,
    currentPage,
    virtualData,
    virtualContainerProps,
    virtualWrapperProps
  }
}
