<template>
  <v-container fluid grid-list-lg class="px-1">
    <v-layout row wrap>
        <v-flex xs12 sm6 md4 lg3 v-for="match in quarters" :key="`match-card-${match.id}`">
          <match-card :match="match" knockoutPhase="true"></match-card>
        </v-flex>
      </v-layout>
  </v-container>
</template>

<script>
import MatchCard from './MatchCard';

export default {
  name: 'Quarters',
  components: {
    MatchCard,
  },
  computed: {
    quarters() {
      return this.$store.getters['game/quarters'];
    },
  },
};
</script>

