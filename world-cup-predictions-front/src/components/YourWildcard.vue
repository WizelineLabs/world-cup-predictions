<template>
  <v-container>
    <v-layout row wrap class="wcp-tab-text">
      <v-flex xs12>
        <p>
          Select the team you think will win the World Cup. If you're correct, we
          will add <strong>30 points</strong> to your grand total.
          <br />
          Wildcard selection closes on <strong>{{ $filters.MonthDay(wildcardDate) }}</strong>
          at <strong>{{ $filters.HourMin(wildcardDate) }} local time</strong>.
        </p>
      </v-flex>
    </v-layout>
    <v-layout row wrap justify-center class="mb-4">
      <v-flex xs3 class="text-xs-right">
        <p v-if="matchState === 'locked'" class="mr-3">
          <span class="lock-icon"></span>
          <span class="pl-1">Locked</span>
        </p>
      </v-flex>
    </v-layout>
    <v-layout row wrap class="wcp-tab-text">
      <v-flex xs12>
        <v-row>
          <v-col v-for="team in wildcards" :key="`match-card-${team.id}`" cols="2">
            <wildcard :team="team" :matchState="matchState"></wildcard>
          </v-col>
        </v-row>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import moment from 'moment';
import Wildcard from './Wildcard';

export default {
  name: 'YourWildcard',
  components: {
    Wildcard,
  },
  computed: {
    wildcardDate() {
      return this.$store.getters['wildcardDate'];
    },
    matchStartTime() {
      return moment(this.wildcardDate);
    },
    matchState() {
      if (this.currentTime < this.matchStartTime) return 'open';
      return 'locked';
    },
    wildcards() {
      return this.$store.getters['wildcards'];
    },
  },
  data() {
    return {
      currentTime: moment(),
    };
  },
};
</script>

<style lang="scss">
.wcp-wildcard-text {
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

.lock-icon {
  color: #696969;
  display: inline-block;
  position: relative;
  margin-left: 3px;
  margin-top: 10px;
  width: 13px;
  height: 10px;
  border-radius: 1px;
  border: solid 1px currentColor;
}

.lock-icon::before {
  content: '';
  position: absolute;
  left: 2px;
  top: -8px;
  width: 7px;
  height: 7px;
  border-radius: 4px 4px 0 0;
  border-top: solid 1px currentColor;
  border-left: solid 1px currentColor;
  border-right: solid 1px currentColor;
}

// Responsiveness
.xs {
  .wcp-wildcard-text {
    padding: 8px 0;
  }
}
</style>
