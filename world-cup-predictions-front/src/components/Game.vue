<template>
  <div>
    <v-container v-if="user && user.id">
      <v-layout row wrap justify-center class="mb-4">
        <v-flex xs10>
          <h1 class="display-1 mt-5 mb-4 text--darken-2 grey--text">
            Prediction Game
          </h1>

          <div class="wcp-flex align-center pt-2">
            <v-card class="mx-auto" color="#f9fafc">
              <v-card-item>
                <v-row align="center" no-gutters>
                  <v-col cols="3">
                    <v-avatar color="indigo" size="x-large">
                      <img :src="user.avatar" :alt="user.first_name">
                    </v-avatar>
                  </v-col>
                  <v-col cols="9">
                    <v-card-title>{{ user.first_name }} {{ user.last_name }}</v-card-title>
                    <v-card-subtitle>
                      {{ user.email }}
                    </v-card-subtitle>
                  </v-col>
                </v-row>
              </v-card-item>

              <v-card-text class="mx-auto my-12">
                <v-row align="center" no-gutters>
                  <v-col cols="6">
                    <v-card-title>Correct Predictions</v-card-title>
                  </v-col>
                  <v-col cols="3">
                    <v-card-title>Rank</v-card-title>
                  </v-col>
                  <v-col cols="3">
                    <v-card-title>Score</v-card-title>
                  </v-col>
                </v-row>
                <v-row align="center" no-gutters>
                  <v-col cols="6">
                    <v-card-subtitle>
                      {{ user.correct_votes }} out of {{ user.total_votes }}
                    </v-card-subtitle>
                  </v-col>
                  <v-col cols="3">
                    <v-card-subtitle>{{ user.rank }}</v-card-subtitle>
                  </v-col>
                  <v-col cols="3">
                    <v-card-subtitle>{{ user.score }}</v-card-subtitle>
                  </v-col>
                </v-row>
              </v-card-text>

            </v-card>
          </div>

        </v-flex>
      </v-layout>

      <v-layout wrap justify-center class="mb-4">
        <v-flex xs12 class="mt-2">

          <v-tabs v-model="active" class="solid-tabs mt-3" light color="transparent" hide-slider>
            <v-tab value="1" ripple>
              Predictions
            </v-tab>
            <v-tab value="2" ripple>
              Wildcard
            </v-tab>
            <v-tab value="3" ripple>
              Leaderboard
            </v-tab>
          </v-tabs>
          <v-window v-model="active">
            <v-window-item value="1">
              <your-predictions></your-predictions>
            </v-window-item>
            <v-window-item value="2">
              <your-wildcard></your-wildcard>
            </v-window-item>
            <v-window-item value="3">
              <leaderboard></leaderboard>
            </v-window-item>
          </v-window>

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
