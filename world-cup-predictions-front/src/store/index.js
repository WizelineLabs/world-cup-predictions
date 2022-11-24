import { createStore } from 'vuex'
import user from '@/store/modules/user';
import team from '@/store/modules/team';
import game from '@/store/modules/game';
import leaderboard from '@/store/modules/leaderboard';
import dialog from '@/store/modules/dialog';

const store = createStore({
  state() {
    return {
      user: user.state,
      leaderboard: leaderboard.state,
      dialog: dialog.state,
      ...team.state,
      ...game.state,
    }
  },
  getters: {
    ...user.getters,
    ...team.getters,
    ...game.getters,
    ...leaderboard.getters,
    ...dialog.getters,
  },
  actions: {
    ...user.actions,
    ...team.actions,
    ...game.actions,
    ...leaderboard.actions,
    ...dialog.actions,
  },
  mutations: {
    ...user.mutations,
    ...team.mutations,
    ...game.mutations,
    ...leaderboard.mutations,
    ...dialog.mutations,
  }
});

export default store;
