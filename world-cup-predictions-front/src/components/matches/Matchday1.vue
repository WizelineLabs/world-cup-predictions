<template>
  <v-container fluid grid-list-lg class="px-1">
    <v-layout row wrap>
        <v-flex xs12 sm6 md4 lg3 v-for="match in matchday1" :key="`match-card-${match.id}`">
          <match-card :match="match"></match-card>
        </v-flex>
      </v-layout>
  </v-container>
</template>

<script>
import MatchCard from './MatchCard';

export default {
  name: 'Matchday1',
  components: {
    MatchCard,
  },
  computed: {
    matchday1() {
      return this.$store.getters['game/matchday1'];
    },
  },
};
</script>

