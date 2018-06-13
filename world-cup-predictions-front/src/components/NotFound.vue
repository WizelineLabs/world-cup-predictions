<template>
  <v-container>
    <v-layout row wrap>
      <v-flex xs12>
        <h1>Page Not found</h1>
        <p class="wcp-no-found-text mt-2">
          Return to <router-link to="/">Home</router-link>
        </p>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
export default {
  name: 'NotFound',
};
</script>

<style lang="scss">
.wcp-no-found-text {
  font-size: 18px;
  letter-spacing: 0.2px;
  line-height: 1.5;
  margin: 0;
}
</style>
