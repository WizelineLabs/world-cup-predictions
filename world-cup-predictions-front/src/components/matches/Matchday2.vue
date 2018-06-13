<template>
  <v-container fluid grid-list-lg class="px-1">
    <v-layout row wrap>
        <v-flex xs12 sm6 md4 lg3 v-for="match in matchday2" :key="`match-card-${match.id}`">
          <match-card :match="match"></match-card>
        </v-flex>
      </v-layout>
  </v-container>
</template>

<script>
import MatchCard from './MatchCard';

export default {
  name: 'Matchday2',
  components: {
    MatchCard,
  },
  computed: {
    matchday2() {
      return this.$store.getters['game/matchday2'];
    },
  },
};
</script>

