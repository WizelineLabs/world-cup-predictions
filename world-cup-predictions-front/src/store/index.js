import { createStore } from 'vuex'
import user from '@/store/modules/user';
import team from '@/store/modules/team';
import game from '@/store/modules/game';
import leaderboard from '@/store/modules/leaderboard';
import dialog from '@/store/modules/dialog';

const store = createStore({
  state() {
    return {
      user,
      team,
      game,
      leaderboard,
      dialog,
    }
  },
  actions: {
    ...user.actions
  }
});

export default store;
