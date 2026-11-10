import { createApp } from 'vue';
import App from './App.vue';
import router from './router';

import 'quasar/dist/quasar.css';
import '@quasar/extras/material-icons/material-icons.css';
import './styles/main.scss';
import { Quasar } from 'quasar';
import quasarUserOptions from './quasar-user-options';
import { vReveal } from './reveal.js';

const app = createApp(App);

app.use(router);
app.use(Quasar, quasarUserOptions);
app.directive('reveal', vReveal);

app.mount('#app');
