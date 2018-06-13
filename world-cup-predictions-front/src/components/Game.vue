<template>
  <div>
    <v-container v-if="user && user.id">
      <v-layout row wrap>
        <v-flex xs5>
          <h3 class="headline my-4">
            <v-avatar color="indigo">
              <img :src="user.avatar" :alt="user.first_name">
            </v-avatar>
            <span class="pl-2">{{user.first_name}} {{user.last_name}}</span>
          </h3>
        </v-flex>
        <v-flex xs7 class="text-xs-right pt-36">
          <span class="caption mr-1">CORRECT PREDICTIONS</span>
          <span class="headline mr-5">
            {{user.correct_votes}} out of {{user.finished_matches}}
          </span>
          <span class="caption mr-1">RANK</span>
          <span class="headline mr-5">{{user.rank}}</span>
          <span class="caption mr-1">SCORE</span>
          <span class="headline">{{user.score}}</span>
        </v-flex>
        <v-flex xs12 class="mt-2">
          <h1 class="display-1 mt-4 mb-4 text--darken-2 grey--text">Prediction Game</h1>
          <v-tabs
            class="solid-tabs mt-3"
            v-model="active"
            light
            color="transparent"
            hide-slider
          >
            <v-tab :key="1" ripple>
              Predictions
            </v-tab>
            <v-tab :key="2" ripple>
              Wildcard
            </v-tab>
            <v-tab :key="3" ripple>
              Leaderboard
            </v-tab>
            <v-tabs-items>
              <v-tab-item :key="1">
                <your-predictions></your-predictions>
              </v-tab-item>
              <v-tab-item :key="2">
                <your-wildcard></your-wildcard>
              </v-tab-item>
              <v-tab-item :key="3">
                <leaderboard></leaderboard>
              </v-tab-item>
            </v-tabs-items>
          </v-tabs>
        </v-flex>
      </v-layout>
    </v-container>
  </div>
</template>

<script>
import YourPredictions from './YourPredictions';
import YourWildcard from './YourWildcard';
import Leaderboard from './Leaderboard';

export default {
  name: 'Game',
  components: {
    YourPredictions,
    YourWildcard,
    Leaderboard,
  },
  data() {
    return {
      active: null,
    };
  },
  computed: {
    user() {
      return this.$store.state.user.data;
    },
  },
  created() {
    this.$store.dispatch('user/getUser').then(() => {
      this.$store.dispatch('game/getGames');
      this.$store.dispatch('leaderboard/getLeaderboard');
    });
  },
};
</script>

<style lang="scss">
.pt-36 {
  padding-top: 36px;
}
</style>
