<template>
  <div>
    <v-container v-if="user && user.id" class="mb-5">
      <v-layout row wrap>
        <v-flex xs12 sm12 md5 class="pt-4">
          <div class="wcp-flex align-center pt-2">
            <v-avatar color="indigo">
              <img :src="user.avatar" :alt="user.first_name">
            </v-avatar>
            <span class="wcp-text-24 pl-3">
              {{user.first_name}} {{user.last_name}}
            </span>
          </div>
        </v-flex>
        <v-flex xs12 sm12 md7 class="text-md-right pt-34 hidden-sm-and-down">
          <span class="wcp-text-12 mr-1">CORRECT PREDICTIONS</span>
          <span class="wcp-text-28 mr-5">
            {{user.correct_votes}} out of {{user.total_votes}}
          </span>
          <span class="wcp-text-12 mr-1">RANK</span>
          <span class="wcp-text-28 mr-5">{{user.rank}}</span>
          <span class="wcp-text-12 mr-1">SCORE</span>
          <span class="wcp-text-28">{{user.score}}</span>
        </v-flex>
        <v-flex xs12 sm12 md7 class="pt-4 hidden-md-and-up">
          <v-layout row wrap class="pt-2">
            <v-flex xs6>
              <span class="wcp-text-12 d-block">RANK</span>
              <span class="wcp-text-28">{{user.rank}}</span>
            </v-flex>
            <v-flex xs6>
              <span class="wcp-text-12 d-block">SCORE</span>
              <span class="wcp-text-28">{{user.score}}</span>
            </v-flex>
          </v-layout>
        </v-flex>
        <v-flex xs12 class="mt-2">
          <h1 class="display-1 mt-4 mb-4 text--darken-2 grey--text hidden-sm-and-down">
            Prediction Game
          </h1>
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
            <v-tabs-items touchless>
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
    this.$store.dispatch('getUser').then(() => {
      this.$store.dispatch('getGames');
      this.$store.dispatch('getLeaderboard');
      this.$store.dispatch('getMyLeaderboard');
    });
  },
};
</script>

<style lang="scss">
.pt-34 {
  padding-top: 34px;
}
</style>
