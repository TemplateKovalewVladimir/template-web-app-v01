import '@/plugins/unocss'
import '@/style.less'

import { createApp } from 'vue'
import App from '@/App.vue'
import { setupRouter } from '@/router'
import { setupStore } from '@/store'

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'


const setupAll = async () => {
  const app = createApp(App)

  app.use(ElementPlus)

  setupStore(app)

  setupRouter(app)

  app.mount('#app')
}

setupAll()
