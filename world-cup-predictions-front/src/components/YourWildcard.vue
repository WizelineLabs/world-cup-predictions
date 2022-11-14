<template>
  <v-container>
    <v-layout row wrap class="wcp-wildcard-text">
      <v-flex xs9>
        <p>
          Select the team you think will win the World Cup. If you're correct, we
          will add <strong>30 points</strong> to your grand total.
          <br />
          Wildcard selection closes on <strong>{{$filters.MonthDay(wildcardDate)}}</strong>
          at <strong>{{$filters.HourMin(wildcardDate)}} local time</strong>.
        </p>
      </v-flex>
      <v-flex xs3 class="text-xs-right">
        <p v-if="matchState === 'locked'" class="mr-3">
          <span class="lock-icon"></span>
          <span class="pl-1">Locked</span>
        </p>
      </v-flex>
    </v-layout>
    <v-container fluid grid-list-lg class="px-1 mt-3">
      <v-layout row wrap>
          <v-flex xs6 sm4 md3 lg2 v-for="team in wildcards" :key="`match-card-${team.id}`">
            <wildcard :team="team" :matchState="matchState"></wildcard>
          </v-flex>
        </v-layout>
    </v-container>
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
      return this.$store.getters['game/wildcardDate'];
    },
    matchStartTime() {
      return moment(this.wildcardDate);
    },
    matchState() {
      if (this.currentTime < this.matchStartTime) return 'open';
      return 'locked';
    },
    wildcards() {
      return this.$store.getters['team/wildcards'];
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
