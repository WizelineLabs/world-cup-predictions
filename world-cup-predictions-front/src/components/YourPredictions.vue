<template>
  <v-container>
    <v-layout row wrap class="pa-2 wcp-tab-text">
      <v-flex xs12>
        <p>
          For each right guess, you’ll be granted <strong>10 points</strong>. Paul's prediction
          for the matchup will be visible once your vote is locked and the match is in progress.
        </p>
      </v-flex>
      <v-flex xs12 >
        <v-tabs
            class="solid-tabs nested-tabs"
            v-model="active"
            light
            color="transparent"
            hide-slider
          >
            <v-tab :key="1">
              Group Round: 1
            </v-tab>
            <v-tab :key="2">
              Group Round: 2
            </v-tab>
            <v-tab :key="3">
              Group Round: 3
            </v-tab>
            <v-tab :key="4" disabled>
              Round of 16
            </v-tab>
            <v-tab :key="5" disabled>
              Quarters
            </v-tab>
            <v-tab :key="6" disabled>
              Semis
            </v-tab>
            <v-tab :key="7" disabled>
              3rd & Final
            </v-tab>
            <v-tabs-items class="mt-4">
              <v-tab-item :key="1">
                <matchday1></matchday1>
              </v-tab-item>
              <v-tab-item :key="2">
                <matchday2></matchday2>
              </v-tab-item>
              <v-tab-item :key="3">
                <matchday3></matchday3>
              </v-tab-item>
              <v-tab-item :key="4">
                <round-of16></round-of16>
              </v-tab-item>
              <v-tab-item :key="5">
                <quarters></quarters>
              </v-tab-item>
              <v-tab-item :key="6">
                <semis></semis>
              </v-tab-item>
              <v-tab-item :key="7">
                <final></final>
              </v-tab-item>
            </v-tabs-items>
          </v-tabs>
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
      active: null,
    };
  },
};
</script>

<style lang="scss">
.wcp-tab-text {
  font-size: 16px;
  font-weight: normal;
  line-height: 1.5;
  color: #424242;

  strong {
    font-weight: 500;
    color: #000000;
  }
}

.solid-tabs.nested-tabs {
  .tabs__wrapper {
    margin-left: -12px;
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
</style>
