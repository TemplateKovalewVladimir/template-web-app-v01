import 'virtual:uno.css'
import 'virtual:svg-icons-register'
import '@/styles/index.less'
import '@imengyu/vue3-context-menu/lib/vue3-context-menu.css'
import 'element-plus/dist/index.css'
import '@/permission'

import dayjs from 'dayjs'
import dayjsRU from 'dayjs/locale/ru'
import ElementPlus from 'element-plus'
import ru from 'element-plus/dist/locale/ru.mjs'
import { createApp } from 'vue'

import App from '@/App.vue'
import { setupRouter } from '@/router'
import { setupStore } from '@/store'

const setupAll = async () => {
  const app = createApp(App)

  dayjs.locale({ ...dayjsRU, weekStart: 1 })
  app.use(ElementPlus, { locale: ru, weekStart: 1 })

  setupStore(app)

  setupRouter(app)

  app.mount('#app')
}

setupAll()
