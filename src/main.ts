import { createApp } from 'vue'
import './style.css'
import App from './App.vue'

const setupAll = async () => {
    const app = createApp(App)

    app.mount('#app')
}

setupAll()
