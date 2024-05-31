
import 'quasar/dist/quasar.css'
import '@quasar/extras/material-icons/material-icons.css'

import { Notify } from 'quasar'

export default {
  plugins: {
    Notify
  },
  config: {
    notify: {} // Optional global config for Notify
  }
}
