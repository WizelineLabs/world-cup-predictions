import Vue from 'vue';
import Vuex from 'vuex';
import user from '@/store/modules/user';
import team from '@/store/modules/team';
import game from '@/store/modules/game';
import leaderboard from '@/store/modules/leaderboard';
import dialog from '@/store/modules/dialog';

Vue.use(Vuex);

const store = new Vuex.Store({
  modules: {
    user,
    team,
    game,
    leaderboard,
    dialog,
  },
});

export default store;
