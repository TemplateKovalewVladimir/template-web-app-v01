import '@/plugins/unocss'
import '@/styles/index.less'

import { createApp } from 'vue'
import App from '@/App.vue'
import { setupRouter } from '@/router'
import { setupStore } from '@/store'

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

import '@/permission'

const setupAll = async () => {
  const app = createApp(App)

  app.use(ElementPlus)

  setupStore(app)

  setupRouter(app)

  app.mount('#app')
}

setupAll()
