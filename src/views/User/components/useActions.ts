import { useEventBus } from '@vueuse/core'
import { FormInstance } from 'element-plus'
import { cloneDeep, isEqual } from 'lodash-es'
import { computed, onMounted, Ref, ref, watch } from 'vue'
import { useRouter } from 'vue-router'

import { Response } from '@/api/utils/request'
import { validateForm } from '@/utils/is'
import { loadingWrapper } from '@/utils/loading'
import { Message } from '@/utils/message'

import { ActionType, EventBusActionKeyType } from './types'

function getObjectDifference(obj1: any, obj2: any): any {
  const diffObj: any = {}

  for (const key in obj1) {
    if (!obj2.hasOwnProperty(key)) {
      diffObj[key] = null
    }
  }

  for (const key in obj2) {
    if (!obj1.hasOwnProperty(key)) {
      diffObj[key] = obj2[key]
    } else {
      if (!isEqual(obj1[key], obj2[key])) diffObj[key] = obj2[key]
    }
  }

  return diffObj
}

type IdDataType = number

export const useActions = <
  GeneralSchema extends { id: number },
  CreateSchema,
  UpdateSchema extends object
>(
  action: ActionType,
  initData: CreateSchema | IdDataType,
  busKey: EventBusActionKeyType,
  backRoute: string,
  getDataFunction: (id: number) => Response<GeneralSchema>,
  createDataFunction: (data: CreateSchema) => Response<GeneralSchema>,
  updateDataFunction: (id: number, data: UpdateSchema) => Response<GeneralSchema>,
  deleteDataFunction: (id: number) => Response<GeneralSchema>
) => {
  if (
    (action === 'create' && typeof initData === 'number') ||
    (action === 'update' && typeof initData !== 'number')
  )
    throw new Error('Type initData is incorrect')

  const router = useRouter()

  const busEvent = useEventBus(busKey)
  const formRef = ref<FormInstance>()
  const loading = ref<boolean>(false)

  const dataSource: Ref<GeneralSchema | CreateSchema | null> = ref(null)
  const dataForm: Ref<GeneralSchema | CreateSchema | null> = ref(null)
  const dataUpdate: Ref<UpdateSchema> = ref({}) as Ref<UpdateSchema>

  const isCreate = computed(() => action === 'create')
  const isUpdate = computed(() => action === 'update')
  const isUpdateEmpty = computed(() => Object.keys(dataUpdate.value).length === 0)

  function cloneData(data) {
    dataSource.value = cloneDeep(data)
    dataForm.value = data
  }

  onMounted(
    loadingWrapper(loading, async () => {
      if (isCreate.value) {
        dataForm.value = initData as CreateSchema
      }
      if (isUpdate.value) {
        const id = initData as number
        const { data } = await getDataFunction(id)
        cloneData(data)

        watch(
          dataForm,
          () => {
            dataUpdate.value = getObjectDifference(dataSource.value, dataForm.value)
          },
          { deep: true }
        )
      }
    })
  )

  const create = loadingWrapper(loading, async () => {
    const { isValid } = await validateForm(formRef.value)
    if (!isValid) throw Error('Ошибка валидации')

    const { data } = await createDataFunction(dataForm.value as CreateSchema)
    Message('Успешно', `Создан ${data.id}`)
    busEvent.emit({ status: 'create' })
    router.push(backRoute)
  })

  const update = loadingWrapper(loading, async () => {
    const { isValid } = await validateForm(formRef.value)
    if (!isValid) throw Error('Ошибка валидации')

    const { data } = await updateDataFunction(
      (dataForm.value as GeneralSchema).id,
      dataUpdate.value
    )
    Message('Успешно', `Изменен ${data.id}`)
    busEvent.emit({ status: 'update' })
    cloneData(data)
  })

  const remove = loadingWrapper(loading, async () => {
    const { data } = await deleteDataFunction((dataForm.value as GeneralSchema).id)
    Message('Успешно', `Удален ${data.id}`)
    busEvent.emit({ status: 'delete' })
    router.push(backRoute)
  })

  return {
    dataForm,
    formRef,
    isCreate,
    isUpdate,
    isUpdateEmpty,
    create,
    update,
    remove,
    loading
  }
}
