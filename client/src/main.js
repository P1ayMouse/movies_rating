import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import "bootstrap"
import "bootstrap/dist/css/bootstrap.css"

import 'quasar/src/css/index.sass'
import { Quasar } from 'quasar'
import quasarUserOptions from './quasar-user-options'

const app = createApp(App)

app.use(router)
app.use(Quasar, quasarUserOptions)

app.mount('#app')
