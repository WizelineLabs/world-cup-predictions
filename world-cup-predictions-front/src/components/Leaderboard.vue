<template>
  <v-container class="wcp-leaderboard mb-5">
    <v-layout row wrap>
      <v-flex xs12 class="mt-3 mb-4 text-xs-right">
        <span class="wcp-text-14">Particpants: </span>
        <span class="wcp-text-14">{{participants}}</span>
      </v-flex>
    </v-layout>

    <!--Table header -->
    <v-layout row class="my-3 wcp-table-row">
      <div class="wcp-table-cell-right">
        <div>
          <v-layout row>
            <v-flex xs2 sm2 md2 class="text-xs-center">
              <span class="caption grey--text text--darken-1">
                RANK
              </span>
            </v-flex>
            <v-flex xs8 sm8 md5>
              <span class="caption grey--text text--darken-1">
                PLAYER
              </span>
            </v-flex>
            <v-flex md3 class="text-xs-right hidden-sm-and-down">
              <span class="caption grey--text text--darken-1">
                CORRECT PREDICTIONS
              </span>
            </v-flex>
            <v-flex xs2 sm2 md2 class="text-xs-right">
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
      <div class="wcp-table-cell-right">
        <div class="wcp-table-row-border" :class="{'current-user': player.isCurrentUser}">
          <v-layout row>
            <v-flex xs2 sm2 md2 class="text-xs-center">
              <v-card flat>
                <v-card-text class="subheading">{{player.rank}}</v-card-text>
              </v-card>
            </v-flex>
            <v-flex xs8 sm8 md5>
              <v-card flat>
                <v-card-text class="subheading">
                  <v-avatar color="grey lighten-2" size="32px" class="mr-2 hidden-xs-only">
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
            <v-flex md3 class="text-xs-right hidden-sm-and-down">
              <v-card flat>
                <v-card-text class="subheading">
                  {{player.correct_votes}} out of {{player.total_votes}}
                  </v-card-text>
              </v-card>
            </v-flex>
            <v-flex xs2 sm2 md2 class="text-xs-right">
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

        if (
          this.user &&
          item.first_name === this.user.first_name &&
          item.last_name === this.user.last_name
        ) {
          item.isCurrentUser = true;
        } else if (
          item.first_name === 'Paul' &&
          item.last_name === 'Prediction'
        ) {
          item.isPaul = true;
          item.avatar = '/static/paul.png';
        }

        return item;
      });
    },
    participants() {
      return this.players.length;
    },
    user() {
      return this.$store.state.user.data;
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

  .current-user {
    background-color: rgba(21, 101, 192, 0.3);
    border-color: transparent;
  }

  .card {
    background-color: transparent;
  }

  .card__text {
    padding: 10px 0;
    line-height: 32px;
  }
}
</style>
