import actions from './actions';
import mutations from './mutations';

const state = {
  list: [],
  myList: [],
};

export default {
  namespaced: true,
  state,
  actions,
  mutations,
};
