import { createApp } from 'vue'

import App from '@/App.vue'

const setupAll = async () => {
  const app = createApp(App)
  app.mount('#app')
}

setupAll()
