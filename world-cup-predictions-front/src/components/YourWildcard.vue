<template>
  <v-container>
    <v-layout row wrap class="pa-2 wcp-wildcard-text">
      <v-flex xs12>
        <p>
          Select the team you think will win the World Cup. If you're correct, we
          will add <strong>30 points</strong> to your grand total.
          <br />
          Wildcard selection closes on <strong>{{wildcardDate | MonthDay}}</strong>
          at <strong>{{wildcardDate | HourMin}} local time</strong>.
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
  font-size: 16px;
  font-weight: normal;
  line-height: 1.5;
  color: #424242;

  strong {
    font-weight: 500;
    color: #000000;
  }
}
</style>
