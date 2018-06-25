<template>
  <v-container fluid grid-list-lg class="px-1">
    <v-layout row wrap>
        <v-flex xs12 sm6 md4 lg3 v-for="match in roundOf16" :key="`match-card-${match.id}`">
          <match-card :match="match" knockoutPhase="true"></match-card>
        </v-flex>
      </v-layout>
  </v-container>
</template>

<script>
import MatchCard from './MatchCard';

export default {
  name: 'RoundOf16',
  components: {
    MatchCard,
  },
  computed: {
    roundOf16() {
      return this.$store.getters['game/roundOf16'];
    },
  },
};
</script>

