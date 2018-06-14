<template>
  <div class="match-card mb-4" :class="[`${matchState}`]">
    <v-layout row wrap>
      <v-flex xs12 text-xs-center class="pt-3 pb-2">
        <span>{{match.date | formatDate}}</span>
      </v-flex>
      <v-flex xs12 text-xs-center class="match-result-container">
        <div class="d-inline-block match-flag-wrapper">
          <div :class="['match-flag', 'flag-icon', `flag-icon-${match.home_flag}`]"></div>
          <span class="match-flag-label d-block mt-2">{{match.home}}</span>
        </div>
        <div class="match-result">
          {{this.matchState !== 'open' ? match.home_score : ''}} -
          {{ this.matchState !== 'open' ? match.away_score : ''}}
        </div>
        <div class="d-inline-block match-flag-wrapper">
          <div :class="['match-flag', 'flag-icon', `flag-icon-${match.away_flag}`]"></div>
          <span class="match-flag-label d-block mt-2">{{match.away}}</span>
        </div>
      </v-flex>
      <v-flex xs12 text-xs-center class="py-1">
        <span class="match-card-label">Paul's Prediction</span>
      </v-flex>
      <v-flex xs12 text-xs-center
        class="grey--text pt-0 pb-1"
        :class="{
          'text--lighten-1': this.matchState === 'open',
          'text--darken-1': this.matchState !== 'open'
        }"
      >
        <div class="match-prediction" v-if="this.matchState === 'open'">?</div>
        <div class="match-prediction" v-else >
          {{match.home_win | percentage}}
        </div>
        <div class="match-prediction" v-if="this.matchState === 'open'">?</div>
        <div class="match-prediction" v-else >
          {{match.draw | percentage}}
        </div>
        <div class="match-prediction" v-if="this.matchState === 'open'">?</div>
        <div class="match-prediction" v-else >
          {{match.away_win | percentage}}
        </div>
      </v-flex>

      <v-flex xs12 text-xs-center>
        <div class="winner-selection-container">
          <label class="winner-selection-button">
            <input
              type="radio"
              :name="`winner-match-${match.id}`"
              value="H"
              :checked="'H' === choiceSelected"
              @click="handleChoiceSelected"
              :disabled="this.matchState !== 'open'"
            />
            <span class="winner-selection-button-check"></span>
            <p class="winner-selection-button-label">WIN</p>
          </label>
        </div>
        <div class="winner-selection-container">
          <label class="winner-selection-button">
            <input
              type="radio"
              :name="`winner-match-${match.id}`"
              value="D"
              :checked="'D' === choiceSelected"
              @click="handleChoiceSelected"
              :disabled="this.matchState !== 'open'"
            />
            <span class="winner-selection-button-check"></span>
            <p class="winner-selection-button-label">DRAW</p>
          </label>
        </div>
        <div class="winner-selection-container">
          <label class="winner-selection-button">
            <input
              type="radio"
              :name="`winner-match-${match.id}`"
              value="A"
              :checked="'A' === choiceSelected"
              @click="handleChoiceSelected"
              :disabled="this.matchState !== 'open'"
            />
            <span class="winner-selection-button-check"></span>
            <p class="winner-selection-button-label">WIN</p>
          </label>
        </div>
      </v-flex>

      <v-flex xs12 text-xs-center class="mt-3">
        <span class="match-caption">{{matchCaption}}</span>
      </v-flex>
    </v-layout>
    <div class="match-card-save-status"
      :class="{
        show: showSaveStatus,
        'status-error': errorSaving
      }">
      {{saveStatus}}
    </div>
  </div>
</template>

<script>
import moment from 'moment';

export default {
  name: 'MatchCard',
  props: ['match'],
  data() {
    return {
      choiceSelected: this.match.choice || '',
      winnerResult: this.match.correct,
      matchStartTime: moment(this.match.date),
      currentTime: moment(),
      saveStatus: '',
      showSaveStatus: false,
      errorSaving: false,
    };
  },
  computed: {
    user() {
      return this.$store.state.user;
    },
    matchState() {
      if (this.currentTime < this.matchStartTime) return 'open';
      else if (this.winnerResult === null || this.winnerResult === '') {
        return 'locked';
      } else if (!this.choiceSelected) return 'no-voted';
      else if (this.winnerResult) return 'correct';
      return 'incorrect';
    },
    matchCaption() {
      moment.updateLocale('en', {
        relativeTime: {
          future: '%s left',
        },
      });
      const relativeTime = moment(this.match.date).fromNow();
      switch (this.matchState) {
        case 'open':
          return `${relativeTime} to cast your vote`;
        case 'locked':
          return 'Match in progress';
        case 'no-voted':
          return 'No vote made';
        case 'correct':
          return 'Nice guess!';
        case 'incorrect':
          return 'Better luck next match!';
        default:
          return '';
      }
    },
    currentGuess() {
      return this.wildcardSelected || this.user.data.winner_choice;
    },
  },
  methods: {
    handleChoiceSelected(event) {
      const value = event.target.value;
      this.choiceSelected = this.choiceSelected === value ? '' : value;

      this.$store
        .dispatch('user/setGuess', {
          game_id: this.match.id,
          choice: this.choiceSelected,
        })
        .then(() => {
          this.$store.dispatch('game/getGames');
          this.saveStatus = 'Prediction Saved!';
          this.showStatus();
        })
        .catch(() => {
          this.saveStatus = "We couldn't save your guess";
          this.showStatus(true);
        });
    },
    showStatus(hasError) {
      const self = this;
      self.showSaveStatus = true;
      self.errorSaving = hasError;
      setTimeout(() => {
        self.showSaveStatus = false;
        self.errorSaving = false;
      }, 3000);
    },
  },
};
</script>

<style lang="scss">
.match-card {
  border-radius: 8px;
  border: solid 1px #adb6c0;
  font-size: 14px;
  padding: 8px;
  position: relative;
}

.match-card-save-status {
  color: #1565c0;
  font-family: 'ProximaNova-Semibold', 'Roboto', sans-serif;
  font-size: 14px;
  font-weight: 500;
  line-height: 1.5;
  letter-spacing: 0.3px;
  opacity: 0;
  position: absolute;
  text-align: center;
  transition: all 0.3s ease-out;
  top: 99%;
  width: 100%;

  &.status-error {
    color: #d32f2f;
  }

  &.show {
    opacity: 1;
    top: 102%;
  }
}

.match-result-container {
  align-items: start;
  display: flex;
  justify-content: center;
}

.match-result {
  display: inline-block;
  font-size: 20px;
  margin: 0 -9px;
  width: 54px;
}

.match-flag-wrapper {
  width: 94px;
}

.match-flag {
  background-color: #adb6c0;
  border-radius: 2px;
  height: 30px;
  line-height: 30px;
  margin: 0;
  position: relative;
  width: 40px;
}

.match-flag-label {
  font-size: 14px;
  letter-spacing: 0;
}

.match-card-label {
  color: #696969;
  font-size: 12px;
  line-height: 1.5;
  letter-spacing: 0.5px;
}

.match-prediction {
  display: inline-block;
  font-size: 16px;
  margin: 0 16px;
  width: 32px;
}

.winner-selection-container {
  display: inline-block;
  margin: 0 16px;
  width: 32px;
}

.winner-selection-button {
  cursor: pointer;
  font-weight: normal;
  position: relative;
  text-align: center;
  user-select: none;
}

.winner-selection-button > input {
  position: absolute;
  opacity: 0;
  cursor: pointer;
}

.winner-selection-button-check {
  align-items: center;
  background-color: #fff;
  border: 1px solid #adb6c0;
  border-radius: 50%;
  display: flex;
  height: 28px;
  justify-content: center;
  width: 28px;
}

.winner-selection-button input:checked ~ .winner-selection-button-check {
  background-color: #1565c0;
  border-color: #1565c0;
}

.winner-selection-button-label {
  font-size: 10px;
  line-height: 18px;
  position: absolute;
  top: 2px;
  width: 28px;
}

.match-caption {
  font-size: 14px;
  font-weight: normal;
  line-height: 1.5;
  letter-spacing: 0.3px;
  color: #696969;
}

.match-card.open {
  .winner-selection-button:hover input ~ .winner-selection-button-check {
    border-color: #1565c0;
  }
}

.match-card.locked {
  background-color: #f1f3f7;
  border-color: #adb6c0;

  .winner-selection-button-check {
    background-color: #eef0f5;
    border-color: #d7dbdf;
  }

  .winner-selection-button input:checked ~ .winner-selection-button-check {
    background-color: #80a3d6;
    border-color: #80a3d6;
  }
}

.match-card.no-voted {
  background-color: #f9fafc;
  border-color: #adb6c0;

  .winner-selection-button-check {
    background-color: #eef0f5;
    border-color: #d7dbdf;
  }
}

.match-card.correct {
  background-color: rgba(21, 101, 192, 0.3);
  border-color: rgba(21, 101, 192, 0.2);

  .match-card-label {
    color: #003c8f;
    opacity: 0.75;
  }

  .match-prediction {
    color: #003c8f;
    opacity: 0.8;
  }

  .winner-selection-button-check {
    background-color: #dbe5f2;
    border-color: #c3cbd8;
  }

  .match-caption {
    color: #1565c0;
    font-weight: 500;
  }
}

.match-card.incorrect {
  background-color: rgba(211, 47, 47, 0.2);
  border-color: rgba(211, 47, 47, 0.15);

  .match-card-label {
    color: #9a0007;
    opacity: 0.75;
  }

  .match-prediction {
    color: #9a0007;
    opacity: 0.75;
  }

  .winner-selection-button-check {
    background-color: #f0e6e8;
    border-color: #d1cdd1;
  }

  .match-caption {
    color: #d32f2f;
    font-weight: 500;
  }

  .winner-selection-button input:checked ~ .winner-selection-button-check {
    background-color: #d32f2f;
    border-color: #d32f2f;
  }
}
</style>

