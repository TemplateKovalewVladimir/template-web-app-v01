import './style.css'

import { createApp } from 'vue'

import App from './App.vue'
import { setupRouter } from './router'

const setupAll = async () => {
  const app = createApp(App)

  setupRouter(app)

  app.mount('#app')
}

setupAll()
