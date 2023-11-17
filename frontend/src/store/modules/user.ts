import { defineStore } from 'pinia'

import { UserSchemaBackend } from '@/api/generated'

interface IUserStore {
  token: string | null
  userInfo: UserSchemaBackend | null
}

export const useUserStore = defineStore('user', {
  state: (): IUserStore => {
    return {
      token: null,
      userInfo: null
    }
  },
  persist: {
    paths: ['token']
  }
})
