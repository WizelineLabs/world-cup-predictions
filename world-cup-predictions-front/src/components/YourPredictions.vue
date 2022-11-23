<template>
  <v-container>
    <v-layout row wrap class="wcp-tab-text">
      <v-flex xs12>
        <p>
          For each right guess, you’ll be granted <strong>10 points</strong>. Paul's prediction
          for the matchup will be visible once your vote is locked and the match is in progress.
        </p>
      </v-flex>
    </v-layout>
    <v-layout row wrap class="wcp-tab-text">
      <v-flex xs12>
        <v-tabs v-model="active" class="solid-tabs nested-tabs" light color="transparent" hide-slider show-arrows>
          <v-tab value="round1">
            Group Round: 1
          </v-tab>
          <v-tab value="round2">
            Group Round: 2
          </v-tab>
          <v-tab value="round3">
            Group Round: 3
          </v-tab>
          <v-tab value="roundOf16">
            Round of 16
          </v-tab>
          <v-tab value="quarters">
            Quarters
          </v-tab>
          <v-tab value="semis">
            Semis
          </v-tab>
          <v-tab value="finals">
            3rd & Final
          </v-tab>
        </v-tabs>
        <v-window v-model="active">
          <v-window-item value="round1">
            <matchday1></matchday1>
          </v-window-item>
          <v-window-item value="round2">
            <matchday2></matchday2>
          </v-window-item>
          <v-window-item value="round3">
            <matchday3></matchday3>
          </v-window-item>
          <v-window-item value="roundOf16">
            <round-of16></round-of16>
          </v-window-item>
          <v-window-item value="quarters">
            <quarters></quarters>
          </v-window-item>
          <v-window-item value="semis">
            <semis></semis>
          </v-window-item>
          <v-window-item value="finals">
            <final></final>
          </v-window-item>
        </v-window>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import Matchday1 from './matches/Matchday1';
import Matchday2 from './matches/Matchday2';
import Matchday3 from './matches/Matchday3';
import RoundOf16 from './matches/RoundOf16';
import Quarters from './matches/Quarters';
import Semis from './matches/Semis';
import Final from './matches/Final';

export default {
  name: 'YourPredictions',
  components: {
    Matchday1,
    Matchday2,
    Matchday3,
    RoundOf16,
    Quarters,
    Semis,
    Final,
  },
  data() {
    return {
      active: '6',
    };
  },
  mounted() {
    setTimeout(() => {
      window.dispatchEvent(new Event('resize'));
    }, 400);
  },
};
</script>

<style lang="scss">
.wcp-tab-text {
  color: #424242;
  font-size: 16px;
  font-weight: normal;
  line-height: 1.5;
  padding: 8px;

  strong {
    font-weight: 500;
    color: #000000;
  }
}

.solid-tabs.nested-tabs {
  width: 100%;

  .tabs__bar {
    margin: 0 -12px;
  }

  .tabs__item {
    font-size: 14px;
    font-weight: normal;
    letter-spacing: 0.3px;
    padding: 6px 12px;
    text-transform: none;
  }

  .tabs__item--active {
    background-color: #fff;
    color: #0d47a1;
  }
}

// Responsiveness
.xs {
  .wcp-tab-text {
    padding: 8px 0;
  }

  .solid-tabs.nested-tabs .tabs__bar {
    margin: 0 -16px;
  }
}
</style>
