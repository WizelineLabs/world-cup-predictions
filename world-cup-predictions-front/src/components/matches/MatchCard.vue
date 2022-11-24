<template>
  <v-card class="match-card mb-4" :class="[`${matchState}`]" width="100%">
    <!-- Match data -->
    <v-card-item>
      <v-row align="center" no-gutters>
        <v-col cols="4" class="text-centered">
          <div class="d-inline-block match-flag-wrapper">
            <div :class="['match-flag', 'fi', `fi-${match.home_flag}`]"></div>
            <v-card-title class="match-flag-label d-block mt-2">{{ match.home }}</v-card-title>
          </div>
        </v-col>
        <v-col cols="4" class="text-centered">
          <div class="match-result">
            <div class="wcp-text-20">
              {{ this.matchState !== 'open' ? match.home_score : '0' }} -
              {{ this.matchState !== 'open' ? match.away_score : '0' }}
            </div>
            <div class="wcp-text-14" v-if="match.home_penalties && match.away_penalties">
              ({{ this.matchState !== 'open' && match.home_penalties ? match.home_penalties : '0' }} -
              {{ this.matchState !== 'open' && match.away_penalties ? match.away_penalties : '0' }})
            </div>
          </div>
        </v-col>
        <v-col cols="4" class="text-centered">
          <div class="d-inline-block match-flag-wrapper">
            <div :class="['match-flag', 'fi', `fi-${match.away_flag}`]"></div>
            <v-card-title class="match-flag-label d-block mt-2">{{ match.away }}</v-card-title>
          </div>
        </v-col>
      </v-row>
    </v-card-item>
    <v-card-subtitle class="text-centered">
      {{ $filters.MonthDay(match.date) }}
    </v-card-subtitle>
    <!-- Predictions -->
    <v-card-item>
      <v-card-subtitle v-if="showPaulsPrediction" class="text-centered">Paul's Prediction</v-card-subtitle>
      <v-card-subtitle v-else class="text-centered">Wizeline Trend</v-card-subtitle>
      <v-row align="center" no-gutters>
        <v-col cols="2">
          <button v-if="!showPaulsPrediction" class="match-button" @click="handlePredictionsChange">
            <div class="match-button-title">PP</div>
            <div class="arrow-left icon"></div>
          </button>
        </v-col>
        <v-col cols="3" class="grey--text text-centered" :class="{
          'text--lighten-1': this.matchState === 'open',
          'text--darken-1': this.matchState !== 'open'
        }">
          <div class="match-prediction" v-if="this.matchState === 'open'">?</div>
          <div class="match-prediction" v-else>
            <span v-if="showPaulsPrediction">{{ $filters.percentage(match.home_win) }}</span>
            <span v-else>{{ $filters.percentage(match.home_win_trend) ?? '-' }}</span>
          </div>
        </v-col>
        <v-col cols="2" class="grey--text text-centered" :class="{
          'text--lighten-1': this.matchState === 'open',
          'text--darken-1': this.matchState !== 'open'
        }">
          <template v-if="!knockoutPhase">
            <span v-if="this.matchState === 'open'">?</span>
            <span v-else>
              <template v-if="showPaulsPrediction">
                {{ $filters.percentage(match.draw) }}
              </template>
              <template v-else>
                {{ $filters.percentage(match.draw_trend) ?? '-' }}
              </template>
            </span>
          </template>
        </v-col>
        <v-col cols="3" class="grey--text text-centered" :class="{
          'text--lighten-1': this.matchState === 'open',
          'text--darken-1': this.matchState !== 'open'
        }">
          <div class="match-prediction" v-if="this.matchState === 'open'">?</div>
          <div class="match-prediction" v-else>
            <span v-if="showPaulsPrediction">{{ $filters.percentage(match.away_win) }}</span>
            <span v-else>{{ $filters.percentage(match.away_win_trend) ?? '-' }}</span>
          </div>
        </v-col>
        <v-col cols="2">
          <button v-if="showPaulsPrediction" class="match-button" @click="handlePredictionsChange">
            <div class="match-button-title">WT</div>
            <div class="arrow-right icon"></div>
          </button>
        </v-col>
      </v-row>
    </v-card-item>
    <!-- Actions -->
    <v-card-actions>
      <v-row align="center" no-gutters>
        <v-col cols="2"></v-col>
        <v-col cols="3" class="text-centered">
          <div class="winner-selection-container">
            <label class="winner-selection-button">
              <input type="radio" :name="`winner-match-${match.id}`" value="H" :checked="'H' === choiceSelected"
                @click="handleChoiceSelected" :disabled="this.matchState !== 'open'" />
              <span class="winner-selection-button-check"></span>
              <p class="winner-selection-button-label">WIN</p>
            </label>
          </div>
        </v-col>
        <v-col cols="2" class="text-centered">
          <div class="winner-selection-container">
            <label v-if="!knockoutPhase" class="winner-selection-button">
              <input type="radio" :name="`winner-match-${match.id}`" value="D" :checked="'D' === choiceSelected"
                @click="handleChoiceSelected" :disabled="this.matchState !== 'open'" />
              <span class="winner-selection-button-check"></span>
              <p class="winner-selection-button-label">DRAW</p>
            </label>
          </div>
        </v-col>
        <v-col cols="3" class="text-centered">
          <div class="winner-selection-container">
            <label class="winner-selection-button">
              <input type="radio" :name="`winner-match-${match.id}`" value="A" :checked="'A' === choiceSelected"
                @click="handleChoiceSelected" :disabled="this.matchState !== 'open'" />
              <span class="winner-selection-button-check"></span>
              <p class="winner-selection-button-label">WIN</p>
            </label>
          </div>
        </v-col>
        <v-col cols="2"></v-col>
      </v-row>
    </v-card-actions>
    <v-layout row wrap>

      <v-flex xs12 text-xs-center>
        <span class="match-caption">{{ matchCaption }}</span>
      </v-flex>
    </v-layout>
    <div class="match-card-save-status" :class="{
      show: showSaveStatus,
      'status-error': errorSaving
    }">
      {{ saveStatus }}
    </div>
  </v-card>
</template>

<script>
import moment from 'moment';

export default {
  name: 'MatchCard',
  props: ['match', 'knockoutPhase'],
  data() {
    return {
      choiceSelected: this.match.choice || '',
      winnerResult: this.match.correct,
      matchStartTime: moment(this.match.date),
      currentTime: moment(),
      saveStatus: '',
      showSaveStatus: false,
      errorSaving: false,
      showPaulsPrediction: true,
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
          m: '1 minute',
          h: '1 hour',
          d: '1 day',
          M: '1 month',
          y: '1 year',
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

      console.log("event: ", event);
      console.log("value: ", value);
      console.log("choiceSelected: ", this.choiceSelected);

      this.$store
        .dispatch('setGuess', {
          game_id: this.match.id,
          choice: this.choiceSelected,
        })
        .then(() => {
          this.$store.dispatch('getGames');
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
    handlePredictionsChange() {
      this.showPaulsPrediction = !this.showPaulsPrediction;
    },
  },
};
</script>

<style lang="scss">
.text-centered {
  text-align: center;
}

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

.match-prediction-wrapper {
  margin: 0 auto !important;
  width: 172px;
}

.match-prediction {
  display: inline-block;
  font-size: 16px;
  width: 32px;
}

.match-button {
  background-color: rgba(129, 135, 143, 0.12);
  border-radius: 2px;
  color: #929292;
  font-size: 12px;
  font-weight: 500;
  letter-spacing: 0.5px;
  height: 40px;
  width: 40px;

  &:hover {
    opacity: 0.75;
  }

  .match-button-title {
    margin-top: -10px;
  }
}

.arrow-left.icon {
  color: #929292;
  position: absolute;
  margin-left: -10px;
  margin-top: 3px;
  width: 16px;
  height: 2px;
  transform: scale(0.6);
  background-color: currentColor;
}

.arrow-left.icon:before {
  content: '';
  position: absolute;
  left: 1px;
  top: -4px;
  width: 10px;
  height: 10px;
  border-top: solid 2px currentColor;
  border-right: solid 2px currentColor;
  -webkit-transform: rotate(-135deg);
  transform: rotate(-135deg);
}

.arrow-right.icon {
  color: #929292;
  position: absolute;
  margin-left: -4px;
  margin-top: 3px;
  width: 16px;
  height: 2px;
  transform: scale(0.6);
  background-color: currentColor;
}

.arrow-right.icon:before {
  content: '';
  position: absolute;
  right: 1px;
  top: -4px;
  width: 10px;
  height: 10px;
  border-top: solid 2px currentColor;
  border-right: solid 2px currentColor;
  -webkit-transform: rotate(45deg);
  transform: rotate(45deg);
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

.winner-selection-button>input {
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

.winner-selection-button input:checked~.winner-selection-button-check {
  background-color: #1565c0;
  border-color: #1565c0;
}

.winner-selection-button-label {
  font-size: 10px;
  line-height: 18px;
  margin-top: 2px;
  margin-bottom: 0;
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
  .winner-selection-button:hover input~.winner-selection-button-check {
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

  .winner-selection-button {
    cursor: default;
  }

  .winner-selection-button input:checked~.winner-selection-button-check {
    background-color: #80a3d6;
    border-color: #80a3d6;
  }

  .match-button {
    background-color: rgba(129, 135, 143, 0.12);
    color: #929292;
  }

  .arrow-left,
  .arrow-right {
    color: #929292;
  }
}

.match-card.no-voted {
  background-color: #f9fafc;
  border-color: #adb6c0;

  .winner-selection-button {
    cursor: default;
  }

  .winner-selection-button-check {
    background-color: #eef0f5;
    border-color: #d7dbdf;
  }

  .match-button {
    background-color: rgba(129, 135, 143, 0.1);
    color: #929292;
  }

  .arrow-left,
  .arrow-right {
    color: #929292;
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

  .winner-selection-button {
    cursor: default;
  }

  .winner-selection-button-check {
    background-color: #dbe5f2;
    border-color: #c3cbd8;
  }

  .match-caption {
    color: #1565c0;
    font-weight: 500;
  }

  .match-button {
    background-color: rgba(21, 101, 192, 0.2);
    color: #708BB9;
  }

  .arrow-left,
  .arrow-right {
    color: #708BB9;
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

  .winner-selection-button {
    cursor: default;
  }

  .winner-selection-button-check {
    background-color: #f0e6e8;
    border-color: #d1cdd1;
  }

  .match-caption {
    color: #d32f2f;
    font-weight: 500;
  }

  .winner-selection-button input:checked~.winner-selection-button-check {
    background-color: #d32f2f;
    border-color: #d32f2f;
  }

  .match-button {
    background-color: rgba(211, 47, 47, 0.15);
    color: #BB7673;
  }

  .arrow-left,
  .arrow-right {
    color: #BB7673;
  }
}
</style>

