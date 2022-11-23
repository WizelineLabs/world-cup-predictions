<template>
  <v-dialog v-model="isOpen" fullscreen hide-overlay transition="dialog-bottom-transition" scrollable>
    <v-card tile>
      <v-toolbar card dark color="red darken-2">
        <v-btn icon dark @click.stop="handleDialog">
          <v-icon>close</v-icon>
        </v-btn>
        <v-toolbar-title class="wcp-toolbar-title">Prediction Model</v-toolbar-title>
        <v-spacer></v-spacer>
      </v-toolbar>
      <div class="wcp-full-container">
        <object data="/static/World_Cup_Predictions.pdf" type="application/pdf" class="wcp-full-container">
          <a href="/static/World_Cup_Predictions.pdf" target="_blank">
            World_Cup_Predictions.pdf
          </a>
        </object>
      </div>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: 'DocDialog',
  computed: {
    isOpen() {
      return this.$store.state.dialog.open;
    },
  },
  methods: {
    handleDialog() {
      this.$store.dispatch('toggle');
    },
  },
};
</script>

<style lang="scss">
.wcp-toolbar-title {
  font-family: 'ProximaNova-Semibold', 'Roboto', sans-serif;
}
</style>
