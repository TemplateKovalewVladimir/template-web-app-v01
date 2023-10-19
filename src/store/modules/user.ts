import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => {
    return {
      token: null as string | null
    }
  },
  persist: {
    enabled: true
  }
})
