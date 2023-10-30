import '@/plugins/unocss'
import '@/styles/index.less'

import { createApp } from 'vue'
import App from '@/App.vue'
import { setupRouter } from '@/router'
import { setupStore } from '@/store'

import ElementPlus from 'element-plus'
import ru from 'element-plus/dist/locale/ru.mjs'
import 'element-plus/dist/index.css'

import '@imengyu/vue3-context-menu/lib/vue3-context-menu.css'

import '@/permission'

const setupAll = async () => {
  const app = createApp(App)

  app.use(ElementPlus, { locale: ru })

  setupStore(app)

  setupRouter(app)

  app.mount('#app')
}

setupAll()
