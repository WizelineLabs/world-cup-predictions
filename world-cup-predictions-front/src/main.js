// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue';
import axios from 'axios';
import moment from 'moment';
import App from './App';
import router from './router';
import store from './store';

const WCP_TOKEN = 'wcp-token';

Vue.config.productionTip = false;
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
Vue.filter('formatDate', (value) => {
  if (value) {
    return moment(String(value)).format('MMMM DD, H:mm');
  }
  return value;
});

Vue.filter('MonthDay', (value) => {
  if (value) {
    return moment(String(value)).format('MMMM Do');
  }
  return value;
});

Vue.filter('HourMin', (value) => {
  if (value) {
    return moment(String(value)).format('H:mm');
  }
  return value;
});

Vue.filter('percentage', (value) => {
  if (value !== null && value !== undefined) {
    const percentage = (value * 100).toFixed(0);
    return `${percentage}%`;
  }
  return value;
});

// Init App
// eslint-disable-next-line
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>',
  store,
});
