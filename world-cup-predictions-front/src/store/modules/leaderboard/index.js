import actions from './actions';
import mutations from './mutations';

const state = {
  list: [],
};

export default {
  namespaced: true,
  state,
  actions,
  mutations,
};
