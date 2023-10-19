import { useUserStore } from '@/store/modules/user'
import { Message } from '@/utils/message'
import axios, { AxiosResponse } from 'axios'

export type Response<T> = Promise<AxiosResponse<T, any>>

const userStore = useUserStore()

// create an axios instance
const request = axios.create({
  baseURL: 'http://api.test.iz2vekdev-u.aa.aliter.spb.ru/',
  timeout: 5000
})

// Для авторизации
request.interceptors.request.use(
  (config) => {
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
    const response = error?.response
    const status = response?.status

    // Проверка авторизации
    if (status === 401) {
      userStore.$reset()
      // router.push({ name: 'login' }).then()
    }

    // Обработка ошибок
    if (response) {
      const data = response?.data?.error
      const msg = data ? data?.detail : 'Ошибка :('
      const title = `Ошибка ${status}`
      Message(title, msg, 'error')
      return Promise.reject(new Error(`${title}: ${msg}`))
    }
    Message(`Необработанная ошибка: ${error}`, 'error')
    return Promise.reject(error)
  }
)

export default request
