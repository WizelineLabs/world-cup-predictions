<template>
  <v-app id="app">
    <v-toolbar flat extended fixed class="wcp-navbar" extension-height="64px">
      <v-container class="py-0">
        <v-layout row wrap class="mt-3 pt-1">
          <v-flex xs8>
            <div class="headline pt-2">
              <img src="/static/wizeline-logo.svg" alt="Wizeline" />
              <span class="pl-2">Prediction Game</span>
              <span class="grey--text text--darken-1 pl-1">Russia World Cup 2018</span>
            </div>
          </v-flex>
          <v-flex xs4 class="text-sm-right">
            <div v-if="!user || !user.id" class="wcp-navbar-text d-inline-block">
              Join the game!
            </div>
            <v-btn
              v-if="user && user.id"
              class="wcp-btn px-2 grey lighten-1 white--text text-transform-none"
              @click="signOut"
            >
              Sign Out
            </v-btn>
            <v-btn
              v-else
              class="wcp-btn px-2 red darken-2 white--text text-transform-none"
              @click="signIn
            ">
              Sign In
            </v-btn>
          </v-flex>
        </v-layout>
        <v-layout row wrap class="mt-1">
          <v-flex xs12>
            <v-tabs
              class="wcp-navbar-tabs mt-2"
              slot="extension"
              color="white"
              slider-color="red"
              @input="handleTabsChange"
            >
              <v-tab
                class="text-transform-none"
                key="home"
                to="/"
                router
              >
                Home
              </v-tab>
              <v-tab
                class="text-transform-none"
                key="about"
                to="/about"
                router
              >
                About the Game
              </v-tab>
              <v-tab
                class="text-transform-none"
                key="prediction"
                to="/prediction"
                router
              >
                Prediction Tool
              </v-tab>
              <v-tab
                v-if="user && user.id"
                class="text-transform-none"
                key="game"
                to="/game"
                router
              >
                Prediction Game
              </v-tab>
            </v-tabs>
          </v-flex>
        </v-layout>
      </v-container>
    </v-toolbar>
    <div class="wcp-body-container">
      <v-slide-x-reverse-transition >
        <router-view/>
      </v-slide-x-reverse-transition>
    </div>
    <doc-dialog></doc-dialog>
  </v-app>
</template>

<script>
import Vue from 'vue';
import DocDialog from './components/DocDialog';

const POPUP_CLOSED = 'popup_closed_by_user';

export default {
  name: 'App',
  components: {
    DocDialog,
  },
  computed: {
    user() {
      return this.$store.state.user.data;
    },
  },
  methods: {
    signIn() {
      Vue.googleAuth().signIn(this.onSignInSuccess, this.onSignInError);
    },
    signOut() {
      Vue.googleAuth().signOut(
        () => {
          this.$store.dispatch('user/logoutUser').then(() => {
            this.$router.push({ path: '/' });
          });
        },
        (error) => {
          this.$store.dispatch('user/setLoginMessage', error);
          this.$router.push({ path: '/' });
        },
      );
    },
    onSignInSuccess(googleUser) {
      const authResponse = googleUser.getAuthResponse();
      const data = {
        access_token: authResponse.access_token,
      };

      this.$store.dispatch('user/loginUser', data).then(
        () => {
          this.$store.dispatch('user/getUser').then(() => {
            this.$router.push({ path: '/game' });
          });
        },
        (error) => {
          this.$store.dispatch('user/setLoginMessage', error.data.message);
        },
      );
    },
    onSignInError(error) {
      if (error.error !== POPUP_CLOSED) {
        this.$store.dispatch('user/setLoginMessage', error);
      }
    },
    handleTabsChange() {
      setTimeout(() => window.scrollTo(0, 0), 300);
    },
  },
  created() {
    this.$store.dispatch('user/fetchLocalUser');
    this.$store.dispatch('team/getTeams');
  },
};
</script>

<style lang="scss">
@import 'vuetify/dist/vuetify.min.css';
@import 'flag-icon-css/css/flag-icon.min.css';

@font-face {
  font-family: 'ProximaNova-Semibold';
  src: url('/static/fonts/ProximaNova-Semibold.eot');
  src: url('/static/fonts/ProximaNova-Semibold.eot?#iefix')
      format('embedded-opentype'),
    url('/static/fonts/ProximaNova-Semibold.svg#ProximaNova-Semibold')
      format('svg');
  font-weight: 600;
  font-style: normal;
}

.application {
  font-family: 'ProximaNova', 'Roboto', sans-serif;

  &.theme--light {
    background-color: #f9fafc;
  }
}

.wcp-full-container {
  height: 100%;
  width: 100%;
}

.wcp-body-container {
  padding-top: 129px;
}

.toolbar.wcp-navbar {
  background-color: #fefefe;
  border-bottom: 1px solid #dcdedf;

  .wcp-navbar-text {
    font-size: 18px;
    letter-spacing: 0.2px;
    line-height: 1.5;
  }
}

.wcp-btn {
  font-family: 'ProximaNova-Semibold', 'Roboto', sans-serif;
  font-size: 17px;
  font-weight: 500;
  letter-spacing: 0.2px;
  line-height: 1.5;
}

.text-transform-none {
  text-transform: none;
}

.wcp-navbar-tabs {
  .tabs__slider {
    height: 4px;
  }

  .tabs__div {
    font-size: 20px;
    font-weight: 400;
    text-transform: none;

    > .tabs__item {
      padding: 0 16px;
    }
  }
}

.solid-tabs {
  .tabs__items {
    background-color: #fff;
  }

  .tabs__div {
    max-width: 310px;
  }

  .tabs__item {
    font-size: 18px;
    font-weight: normal;
    letter-spacing: 0.2px;
    padding: 12px 24px;
    text-transform: none;
  }

  .tabs__item--active {
    background-color: #fff;
  }
}

.wcp-title {
  font-size: 32px;
  font-weight: normal;
  line-height: 1.25;
}

.wcp-text {
  font-size: 18px;
  line-height: 1.5;
  letter-spacing: 0.2px;

  a {
    text-decoration: none;

    &:hover {
      text-decoration: underline;
    }
  }
}

.wcp-subtext {
  font-size: 16px;
  line-height: 1.5;
}

.wcp-caption {
  font-size: 14px;
}
</style>
