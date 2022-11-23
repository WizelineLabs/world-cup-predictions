<template>
  <v-container class="mb-5">
    <v-layout row wrap>
      <v-flex xs12>
        <h1 class="display-1 mt-5 mb-4 text--darken-2 grey--text">Prediction Tool</h1>
        <p class="wcp-text my-4">
          The prediction system estimates the probabilities of each team making it through
          each of the rounds and ultimately winning the World Cup. You can keep track of
          your favorite team's chances making it through the groups stage and the knockout
          phase.
          <br /><br />
          For more information on how our model works, have a look at our
          <a @click.stop="handleDialog">full documentation</a>.
        </p>
        <v-tabs v-model="active" class="solid-tabs mt-3" color="#0d47a1" hide-slider>
          <v-tab value="1">
            Group Stage
          </v-tab>
          <v-tab value="2">
            Knockout Phase
          </v-tab>
        </v-tabs>
        <v-window v-model="active">
          <v-window-item value="1">
            <group-stage></group-stage>
          </v-window-item>
          <v-window-item value="2">
            <knockout-phase></knockout-phase>
          </v-window-item>
        </v-window>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import GroupStage from './GroupStage';
import KnockoutPhase from './KnockoutPhase';

export default {
  name: 'Prediction',
  components: {
    GroupStage,
    KnockoutPhase,
  },
  data() {
    return {
      active: null,
    };
  },
  methods: {
    handleDialog() {
      this.$store.dispatch('toggle');
    },
  },
};
</script>

<style lang="scss">

</style>
