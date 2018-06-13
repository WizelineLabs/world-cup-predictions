import actions from './actions';
import mutations from './mutations';

const state = {
  open: false,
};

export default {
  namespaced: true,
  state,
  actions,
  mutations,
};
