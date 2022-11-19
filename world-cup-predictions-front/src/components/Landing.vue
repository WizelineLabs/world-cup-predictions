<template>
  <v-container>
    <v-layout row wrap justify-center>
      <v-flex xs12 class="text-xs-center">
        <h1 class="wcp-landing-title mt-5 blue--text text--darken-4">
          Predict the Qatar World Cup!
        </h1>
        <h3 class="wcp-landing-subtitle mt-3 grey--text text--darken-2">
          Place your votes, beat Paul and win the game.
        </h3>
      </v-flex>
      <v-flex xs12 class="mt-3 mb-5 text-xs-center">
        <div class="wcp-illustration pt-2">
          <v-btn
            large
            v-if="!user || !user.id"
            class="wcp-btn-lg red darken-2 white--text text-transform-none mt-4"
            @click="signIn"
          >
            Join the game!
          </v-btn>
          <v-btn v-else
            large
            class="wcp-btn-lg red darken-2 white--text text-transform-none mt-4"
            @click="goToGame"
          >
            Join the game!
          </v-btn>
          <p class="wcp-subtext mt-2">
            Open to Wizeliners across all offices and Wizeline Teams.
          </p>
        </div>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>

import { googleTokenLogin } from "vue3-google-login"

const POPUP_CLOSED = 'popup_closed_by_user';

export default {
  name: 'Landing',
  computed: {
    status() {
      return this.$store.state.user.loginMessage;
    },
    user() {
      return this.$store.state.user.data;
    },
  },
  methods: {
    signIn() {
      googleTokenLogin().then(this.onSignInSuccess).catch(this.onSignInError)
    },
    onSignInSuccess(response) {
      const data = {
        access_token: response.access_token,
      };

      this.$store.dispatch('loginUser', data).then(
        () => {
          this.$store.dispatch('getUser').then(() => {
            this.$router.push({ path: '/game' });
          });
        },
        (error) => {
          this.$store.dispatch('setLoginMessage', error.data.message);
        },
      );
    },
    onSignInError(error) {
      if (error.error !== POPUP_CLOSED) {
        this.$store.commit('setLoginMessage', error);
      }
    },
    goToGame() {
      this.$router.push({ path: '/game' });
    },
  },
};
</script>

<style lang="scss">
.wcp-landing-title {
  font-family: 'ProximaNova-Semibold', 'Roboto', sans-serif;
  font-size: 40px;
  font-weight: 600;
  line-height: 1.13;
}

.wcp-landing-subtitle {
  font-size: 24px;
  font-weight: normal;
  line-height: 1.25;
}

.wcp-illustration {
  background-image: url('../assets/home_illustration.svg');
  background-position-y: center;
  background-size: contain;
  display: inline-block;
  height: 431px;
  max-width: 765px;
  width: 100%;
}

.wcp-btn-lg {
  width: 227px;
  height: 54px;
  border-radius: 4px;
  font-family: 'ProximaNova-Semibold', 'Roboto', sans-serif;
  font-size: 24px;
  line-height: 1.25;
  letter-spacing: 1px;
}

// Responsiveness
.xs {
  .wcp-landing-title {
    font-size: 34px;
  }

  .wcp-landing-subtitle {
    font-size: 20px;
  }
}
</style>
