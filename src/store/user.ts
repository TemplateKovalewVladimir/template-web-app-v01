import { defineStore } from 'pinia'

interface State {
  user: UserInfo | null
  role: string[]
}

interface UserInfo {
  id: number
  name: string
}

export const useUserStore = defineStore('user', {
  state: (): State => {
    return {
      user: null,
      role: []
    }
  },
  persist: {
    enabled: true
  }
})
