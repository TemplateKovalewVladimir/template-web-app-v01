import '@/plugins/unocss'
import '@/styles/index.less'

import { createApp } from 'vue'
import App from '@/App.vue'
import { setupI18n } from '@/plugins/vueI18n'
import { setupRouter } from '@/router'
import { setupStore } from '@/store'

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

const setupAll = async () => {
  const app = createApp(App)

  await setupI18n(app)

  app.use(ElementPlus)

  setupStore(app)

  setupRouter(app)

  app.mount('#app')
}

setupAll()
