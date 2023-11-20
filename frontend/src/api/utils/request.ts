import axios, { AxiosResponse } from 'axios'

import { useUserStore } from '@/store/modules/user'
import { Message } from '@/utils/message'

export type Response<T> = Promise<AxiosResponse<T, any>>

export function getQueryPaginateSortFilters({ page, size, sort, filters }) {
  return {
    page: JSON.stringify({ current: page, size }),
    sort: JSON.stringify(sort),
    filters: JSON.stringify(filters)
  }
}

// create an axios instance
export const request = axios.create({
  baseURL: import.meta.env.APP_BASE_API_URL,
  timeout: 60 * 1000 // ms
})

// Для авторизации
request.interceptors.request.use(
  (config) => {
    const userStore = useUserStore()

    if (userStore.token) {
      config.headers['X-API-Key'] = userStore.token
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Обработка ошибок
request.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    const userStore = useUserStore()

    const response = error?.response
    const status = response?.status

    // Проверка авторизации
    if (status === 401) {
      userStore.$reset()
    }

    // Обработка ошибок
    if (response) {
      const data = response?.data?.error
      const msg = data ? data?.detail : 'Ошибка :('
      const title = `Ошибка ${status}`
      Message(title, msg, 'error')
      return Promise.reject(new Error(`${title}: ${msg}`))
    }
    Message(`Необработанная ошибка`, error, 'error')
    return Promise.reject(error)
  }
)
