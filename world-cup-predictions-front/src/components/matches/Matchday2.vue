<template>
  <v-container fluid grid-list-lg class="px-1">
    <v-row>
      <v-col v-for="match in matchday2" :key="`match-card-${match.id}`" cols="4">
        <match-card :match="match"></match-card>
      </v-col>
    </v-row>
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
      return this.$store.getters['matchday2'];
    },
  },
};
</script>

