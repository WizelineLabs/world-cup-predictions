// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import { createApp } from 'vue';
import axios from 'axios';
import moment from 'moment';
import GoogleSignInPlugin from "vue3-google-signin"
import App from './App';
import router from './router';
import store from './store';
// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

const vuetify = createVuetify({
  components,
  directives,
})

const WCP_TOKEN = 'wcp-token';

//Vue.config.productionTip = false;
axios.defaults.withCredentials = true;

// Interceptors
axios.interceptors.response.use(
  // eslint-disable-next-line
  (response) => response.data,
  (error) => {
    if (error.response.status === 401) {
      localStorage.removeItem(WCP_TOKEN);
      router.replace({ path: '/' });
    }
    if (error.response.status === 403) {
      router.replace({ path: '/' });
    }
    return Promise.reject(error.response);
  },
);

// Filters
const filters = {
  formatDate(value) {
    if (value) {
      return moment(String(value)).format('MMMM DD, H:mm');
    }
    return value;
  },
  MonthDay(value) {
    if (value) {
      return moment(String(value)).format('MMMM Do');
    }
    return value;
  },
  HourMin(value){
    if (value) {
      return moment(String(value)).format('H:mm');
    }
    return value;
  },
  percentage(value) {
    if (value !== null && value !== undefined) {
      const percentage = Math.floor(value * 100);
      return `${percentage}%`;
    }
    return value;
  }
}

const app = createApp(App).
  use(router).
  use(store).
  use(vuetify);

app.config.globalProperties.$filters = filters
app.use(GoogleSignInPlugin, {
  clientId: import.meta.env.VITE_GOOGLE_AUTH_KEY,
});

app.mount('#app')