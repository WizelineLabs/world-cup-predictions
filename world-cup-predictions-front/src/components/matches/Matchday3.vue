<template>
  <v-container fluid grid-list-lg class="px-1">
    <v-row>
      <v-col v-for="match in matchday3" :key="`match-card-${match.id}`" cols="4">
        <match-card :match="match"></match-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import MatchCard from './MatchCard';

export default {
  name: 'Matchday3',
  components: {
    MatchCard,
  },
  computed: {
    matchday3() {
      return this.$store.getters['matchday3'];
    },
  },
};
</script>

