import { createApp } from 'vue'
import App from './App.vue'
import './assets/app.css'
import router from './router/index.js'
import store from './store'
import axios from 'axios'

axios.defaults.baseURL = 'http://127.0.0.1:8000'

createApp(App).use(store).use(router, axios).mount('#app')
