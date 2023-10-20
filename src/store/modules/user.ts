import { UserSchema } from '@/api/generated'
import { defineStore } from 'pinia'

interface IUserStore {
  token: string | null
  userInfo: UserSchema | null
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
