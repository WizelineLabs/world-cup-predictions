<template>
  <v-container class="wcp-leaderboard" style="width: 100%;">
    <v-layout row wrap class="pb-2">
      <v-flex xs12 md4>
        <v-select class="search-select mt-1 mb-3" content-class="search-select-content elevation-0" :items="players"
          :filter="customFilter" v-model="selectedPlayer" item-text="fullname" placeholder="Follow your friends..."
          autocomplete append-icon="" solo flat @input="searchSelectHandler">
          <template v-slot:selection="data"></template>
          <template v-slot:item="data">
            <template v-if="data.item.id">
              <v-list-tile-avatar>
                <img :src="data.item.avatar">
              </v-list-tile-avatar>
              <v-list-tile-content>
                <v-list-tile-title v-html="data.item.fullname"></v-list-tile-title>
              </v-list-tile-content>
            </template>
            <template v-else>
              <v-list-tile-content>No data available</v-list-tile-content>
            </template>
          </template>
        </v-select>
      </v-flex>
      <v-flex xs5 md4 class="pt-1">
        <template v-if="followedPlayers.length">
          <span class="wcp-text-16 pl-4 pr-2 hidden-sm-and-down">Toggle View:</span>
          <v-btn small @click="toggleLeaderboard"
            class="elevation-0 grey lighten-2 text-transform-none wcp-text-16 px-1 mx-0">
            {{ followViewActive ? 'Full players list' : 'My list' }}
          </v-btn>
        </template>

      </v-flex>
      <v-flex xs7 md4 class="follow-toolbox pt-1 text-xs-right">
        <template v-if="!followViewActive">
          <span class="wcp-text-14 pt-2 d-inline-block">Participants: </span>
          <span class="wcp-text-14 pt-2">{{ participants }}</span>
        </template>
        <template v-else>
          <v-btn small flat @click="resetFollowList"
            class="indigo--text text--accent-2 text-transform-none wcp-text-16 ml-0 mr-2">
            Reset
          </v-btn>
          <v-btn v-if="!editFollowMode" small flat @click="editFollowList"
            class="indigo--text text--accent-2 text-transform-none wcp-text-16 mx-0">
            Edit
          </v-btn>
          <v-btn v-else small flat @click="doneEditFollowList" class="text-transform-none wcp-text-16 mx-0">
            Done
          </v-btn>
        </template>
      </v-flex>
    </v-layout>

    <!--Table header -->
    <v-row align="center" no-gutters>
      <v-col cols="2" class="text-centered">
        <span class="wcp-text-14 grey--text text--darken-1">
          RANK
        </span>
      </v-col>
      <v-col cols="5" class="text-centered">
        <span class="wcp-text-14 grey--text text--darken-1">
          PLAYER
        </span>
      </v-col>
      <v-col cols="3" class="text-centered">
        <span class="wcp-text-14 grey--text text--darken-1">
          CORRECT PREDICTIONS
        </span>
      </v-col>
      <v-col cols="2" class="text-centered">
        <span class="wcp-text-14 grey--text text--darken-1 pr-5">
          SCORE
        </span>
      </v-col>
      <v-col cols="12" class="text-centered">
        <div class="wcp-table-cell-right" :class="{
          'edit-mode': editFollowMode && followViewActive,
          'transition': followViewActive
        }"></div>
      </v-col>
    </v-row>

    <!--Players list -->
    <v-layout row class="mt-2 wcp-table-row" v-for="player in currentLeaderboard" :key="player._id">
      <v-card class="wcp-table-row-border" :class="{
        'current-user': player.isCurrentUser,
        'is-paul': player.isPaul,
        'top-contender': player.rank === 1
      }">
        <v-row align="center" no-gutters>
          <v-col cols="2" class="text-centered wcp-text-14">
            <span>{{ player.rank }}</span>
          </v-col>
          <v-col cols="1" class="text-centered wcp-text-14">
            <v-avatar color="grey lighten-2" size="32px" class="mr-2 hidden-xs-only">
              <img v-if="player.avatar" :src="player.avatar" :alt="`${player.fullname}`">
            </v-avatar>
          </v-col>
          <v-col cols="4" class="text-centered wcp-text-14">
            <span>{{ player.fullname }}</span>
          </v-col>
          <v-col cols="3" class="text-centered wcp-text-14">
            <span>{{ player.correct_votes }} out of {{ player.total_votes }}</span>
          </v-col>
          <v-col cols="2" class="text-centered wcp-text-14">
            <span>{{ player.score }}</span>
          </v-col>
        </v-row>
      </v-card>
      <div class="wcp-table-cell-right" :class="{
        'edit-mode': editFollowMode && followViewActive,
        'transition': followViewActive
      }">
        <v-btn icon dark color="indigo accent-2" class="elevation-0" @click="removePlayer(player)">
          <v-icon>close</v-icon>
        </v-btn>
      </div>
    </v-layout>

  </v-container>
</template>

<script>
export default {
  name: 'Leaderboard',
  data() {
    return {
      selectedPlayer: null,
      followViewActive: false,
      editFollowMode: false,
      customFilter(item, queryText) {
        // eslint-disable-next-line
        const hasValue = (val) => (val != null ? val : '');
        const text = hasValue(item.fullname);
        const query = hasValue(queryText);
        return (
          text
            .toString()
            .toLowerCase()
            .indexOf(query.toString().toLowerCase()) > -1
        );
      },
    };
  },
  computed: {
    players() {
      const list = this.$store.state.leaderboard.list;
      return this.updateLeaderboardList(list);
    },
    participants() {
      return this.players.length;
    },
    user() {
      return this.$store.state.user.data;
    },
    followedPlayers() {
      const list = this.$store.state.leaderboard.myList;
      const sortedList = list.sort((a, b) => b.score - a.score);
      return this.updateLeaderboardList(sortedList);
    },
    currentLeaderboard() {
      if (this.followViewActive) return this.followedPlayers;
      return this.players;
    },
  },
  methods: {
    updateLeaderboardList(list) {
      return list.map((row) => {
        const item = row;
        item.fullname = `${item.first_name} ${item.last_name}`;

        if (this.user && item.id === this.user.id) {
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
    searchSelectHandler(player) {
      const playerExist = this.followedPlayers.filter(
        // eslint-disable-next-line
        (p) => p.id === player.id,
      );
      if (!playerExist.length) {
        this.$store
          .dispatch('follow', {
            user_id: player.id,
          })
          .then(() => {
            this.$store.dispatch('getMyLeaderboard');
          });
      }
      this.followViewActive = true;
      setTimeout(() => {
        this.selectedPlayer = null;
      }, 0);
    },
    toggleLeaderboard() {
      this.followViewActive = !this.followViewActive;
      this.editFollowMode = false;
    },
    resetFollowList() {
      this.$store.dispatch('unfollowAll').then(() => {
        this.$store.dispatch('getMyLeaderboard').then(() => {
          if (!this.followedPlayers.length) {
            this.editFollowMode = false;
            this.followViewActive = false;
          }
        });
      });
    },
    editFollowList() {
      this.editFollowMode = true;
    },
    doneEditFollowList() {
      this.editFollowMode = false;
    },
    removePlayer(player) {
      this.$store
        .dispatch('unfollow', {
          user_id: player.id,
        })
        .then(() => {
          this.$store.dispatch('getMyLeaderboard').then(() => {
            if (!this.followedPlayers.length) {
              this.editFollowMode = false;
              this.followViewActive = false;
            }
          });
        });
    },
  },
};
</script>

<style lang="scss">
.text-centered {
  text-align: center;
}

.input-group.search-select {
  border-radius: 4px;
  background-color: #fff;
  border: solid 1px #adb6c0;
  max-height: 40px;
  min-height: 40px;

  .input-group--select__autocomplete {
    padding: 0;
  }
}

.search-select-content {
  border-radius: 4px;
  background-color: #fff;
  border: solid 1px #adb6c0;
  margin: 2px 0;

  .list .list__tile--link:hover {
    background-color: rgba(231, 235, 243, 0.3);
  }
}

.wcp-leaderboard {
  .wcp-table-row {
    display: table;
    width: 100%;
  }

  .wcp-table-cell-left {
    display: table-cell;
  }

  .wcp-table-cell-right {
    display: table-cell;
    opacity: 0;
    margin: 0;
    max-width: 0;
    overflow: hidden;
    text-align: center;
    width: 0;

    >.btn {
      height: 24px;
      width: 24px;

      i {
        font-size: 16px;
        padding-left: 1px;
      }
    }

    &.transition {
      transition: all 0.3s ease-out;
    }

    &.edit-mode {
      opacity: 1;
      max-width: 56px;
      width: 56px;
    }
  }

  .wcp-table-row-border {
    border: 1px solid #dcdedf;
    border-radius: 8px;
    overflow: hidden;
  }

  .top-contender {
    background-color: rgba(255, 236, 179, 0.7);
    border: solid 1px rgba(203, 186, 131, 0.4);
  }

  .is-paul {
    background-color: rgba(211, 47, 47, 0.2);
    border: solid 1px rgba(211, 47, 47, 0.15);
  }

  .current-user {
    background-color: rgba(21, 101, 192, 0.3);
    border: solid 1px rgba(21, 101, 192, 0.2);
  }

  .card {
    background-color: transparent;
  }

  .card__text {
    padding: 8px 0;
    line-height: 31px;
  }
}

.follow-toolbox {
  .btn {
    min-width: 61px;
  }
}
</style>
