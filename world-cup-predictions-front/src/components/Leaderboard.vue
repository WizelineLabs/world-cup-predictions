<template>
  <v-container class="wcp-leaderboard mb-5">
    <v-layout row wrap>
      <v-flex xs6 class="mt-3 mb-4 px-4">
        <div class="wcp-dot blue darken-3"></div>
        <span class="wcp-caption mr-4 ml-2">Top Scorers</span>
        <div class="wcp-dot red darken-2"></div>
        <span class="wcp-caption ml-2">Paul (Prediction Tool)</span>
      </v-flex>
      <v-flex xs6 class="mt-3 mb-4 text-xs-right">
        <span class="wcp-caption">Particpants: </span>
        <span class="wcp-caption">{{participants}}</span>
      </v-flex>
    </v-layout>

    <!--Table header -->
    <v-layout row class="my-3 wcp-table-row">
      <div class="wcp-table-cell-left"></div>
      <div class="wcp-table-cell-right">
        <div>
          <v-layout row>
            <v-flex xs2 class="text-xs-center">
              <span class="caption grey--text text--darken-1">
                RANK
              </span>
            </v-flex>
            <v-flex xs5>
              <span class="caption grey--text text--darken-1">
                PLAYER
              </span>
            </v-flex>
            <v-flex xs3 class="text-xs-right">
              <span class="caption grey--text text--darken-1">
                CORRECT PREDICTIONS
              </span>
            </v-flex>
            <v-flex xs2 class="text-xs-right">
              <span class="caption grey--text text--darken-1 pr-5">
                SCORE
              </span>
            </v-flex>
          </v-layout>
        </div>
      </div>
    </v-layout>

    <!--Players list -->
    <v-layout row class="mt-2 wcp-table-row" v-for=" player in players" :key="player._id">
      <div class="wcp-table-cell-left">
        <v-card flat>
          <v-card-text>
            <div
            class="wcp-dot-big"
            :class="{
              'blue darken-3': player.rank === 1 && !player.isPaul,
              'red darken-2': player.isPaul
            }"
          ></div>
          </v-card-text>
        </v-card>
      </div>
      <div class="wcp-table-cell-right">
        <div class="wcp-table-row-border">
          <v-layout row>
            <v-flex xs2 class="text-xs-center">
              <v-card flat>
                <v-card-text class="subheading">{{player.rank}}</v-card-text>
              </v-card>
            </v-flex>
            <v-flex xs5>
              <v-card flat>
                <v-card-text class="subheading">
                  <v-avatar color="grey lighten-2" size="32px" class="mr-2">
                    <img
                      v-if="player.avatar"
                      :src="player.avatar"
                      :alt="`${player.first_name} ${player.last_name}`"
                    >
                  </v-avatar>
                  <span>{{player.first_name}} {{player.last_name}}</span>
                </v-card-text>
              </v-card>
            </v-flex>
            <v-flex xs3 class="text-xs-right">
              <v-card flat>
                <v-card-text class="subheading">
                  {{player.correct_votes}} out of {{player.total_votes}}
                  </v-card-text>
              </v-card>
            </v-flex>
            <v-flex xs2 class="text-xs-right">
              <v-card flat class="pr-5">
                <v-card-text class="subheading">{{player.score}}</v-card-text>
              </v-card>
            </v-flex>
          </v-layout>
        </div>
      </div>
    </v-layout>

  </v-container>
</template>

<script>
export default {
  name: 'Leaderboard',
  computed: {
    players() {
      const list = this.$store.state.leaderboard.list;
      return list.map((row) => {
        const item = row;
        if (item.first_name === 'Paul' && item.last_name === 'Prediction') {
          item.isPaul = true;
          item.avatar = '/static/paul.png';
        }
        return item;
      });
    },
    participants() {
      return this.players.length;
    },
  },
};
</script>

<style lang="scss">
.wcp-dot {
  border-radius: 50%;
  display: inline-block;
  height: 8px;
  width: 8px;
}
.wcp-dot-big {
  border-radius: 50%;
  display: inline-block;
  height: 12px;
  width: 12px;
}

.wcp-leaderboard {
  .wcp-table-row {
    display: table;
    width: 100%;
  }
  .wcp-table-cell-left {
    display: table-cell;
    padding: 0 24px;
    text-align: right;
    width: 60px;
  }

  .wcp-table-cell-right {
    display: table-cell;
  }

  .wcp-table-row-border {
    border: 1px solid #dcdedf;
    border-radius: 8px;
    overflow: hidden;
  }

  .card__text {
    padding: 10px 0;
    line-height: 32px;
  }
}
</style>
