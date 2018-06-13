import actions from './actions';
import getters from './getters';
import mutations from './mutations';

const state = {
  token: null,
  data: {},
  loginMessage: null,
  loginLoading: false,
};

export default {
  namespaced: true,
  state,
  actions,
  getters,
  mutations,
};
