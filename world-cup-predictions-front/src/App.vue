<template>
  <v-app id="app" :class="[`${$vuetify.breakpoint.name}`]">
    <v-toolbar flat fixed class="wcp-navbar" height="140px">
      <v-container class="py-0 my-0">
        <v-layout row wrap class="wcp-navbar-top-container mt-4 pt-1">
          <v-flex xs8>
            <v-layout row wrap>
              <img src="/static/wizeline-logo.svg" alt="Wizeline" />
              <span class="wcp-logo-text wcp-text-16">Prediction Game</span>
              <span
                class="wcp-logo-text wcp-text-16 grey--text text--darken-1 pl-2 hidden-sm-and-down"
              >
                Russia World Cup 2018
              </span>
            </v-layout>
          </v-flex>
          <v-flex xs4 class="text-xs-right">
            <span v-if="!user || !user.id" class="wcp-text-16 pr-2 hidden-sm-and-down">
              Join the game!
            </span>
            <v-btn
              v-if="user && user.id"
              class="wcp-btn grey lighten-1 white--text text-transform-none"
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
        <v-layout row wrap>
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
    <v-dialog v-model="errorDialog" max-width="290">
      <v-card>
        <v-card-title class="headline">Sign in error</v-card-title>
        <v-card-text>
          Please make sure you are signing in with your Wizeline o Wizeline Teams
          account to join the game.
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="red darken-2" flat="flat" @click.stop="closeErrorDialog">
            Cancel
          </v-btn>
          <v-btn color="red darken-2" flat="flat" @click.stop="tryAgainLogin">
            Try again
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
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
  data() {
    return {
      errorDialog: false,
    };
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
          this.errorDialog = true;
          this.$store.dispatch('user/setLoginMessage', error.data.message);
        },
      );
    },
    onSignInError(error) {
      if (error.error !== POPUP_CLOSED) {
        this.errorDialog = true;
        this.$store.dispatch('user/setLoginMessage', error);
      }
    },
    handleTabsChange() {
      setTimeout(() => window.scrollTo(0, 0), 300);
    },
    tryAgainLogin() {
      this.closeErrorDialog();
      this.signIn();
    },
    closeErrorDialog() {
      this.errorDialog = false;
    },
  },
  created() {
    this.$store.dispatch('user/fetchLocalUser');
    this.$store.dispatch('team/getTeams');
  },
};
</script>

<style lang="scss">
@import '../static/css/vuetify.min.css';
//@import 'flag-icon-css/css/flag-icon.min.css';

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

.container {
  margin: auto !important;
}

.wcp-full-container {
  height: 100%;
  width: 100%;
}

.wcp-body-container {
  padding-top: 140px;
  width: 100%;
  overflow-x: hidden;
}

.toolbar.wcp-navbar {
  background-color: #fefefe;
  border-bottom: 1px solid #dcdedf;

  .toolbar__content {
    align-items: start;
  }

  .wcp-navbar-top-container {
    height: 60px;
  }
}

.wcp-logo-text {
  line-height: 28px;
  padding-left: 16px;
}

.wcp-btn {
  font-family: 'ProximaNova-Semibold', 'Roboto', sans-serif;
  font-size: 16px;
  font-weight: 500;
  height: 32px;
  letter-spacing: 0.2px;
  line-height: 1.5;
  margin: 0;
  width: 84px;
}

.wcp-flex {
  display: flex;
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

.wcp-text-28 {
  font-size: 28px;
}

.wcp-text-26 {
  font-size: 26px;
}

.wcp-text-24 {
  font-size: 24px;
}

.wcp-text-22 {
  font-size: 22px;
}

.wcp-text-20 {
  font-size: 20px;
}

.wcp-text-18 {
  font-size: 18px;
}

.wcp-text-16 {
  font-size: 16px;
}

.wcp-text-14 {
  font-size: 14px;
}

.wcp-text-12 {
  font-size: 12px;
}

.wcp-bold {
  font-weight: 500;
}

// Responsiveness
.xs {
  .container {
    padding: 16px;
  }

  .wcp-logo-text {
    padding: 4px 0 0;
    width: 100%;
  }

  .wcp-navbar-tabs {
    position: relative;

    &::before {
      background: linear-gradient(
        -90deg,
        rgba(255, 255, 255, 0.001),
        rgb(255, 255, 255)
      );
      content: '';
      height: 44px;
      left: 0;
      pointer-events: none;
      position: absolute;
      top: 0;
      width: 30px;
      z-index: 10;
    }
    &::after {
      background: linear-gradient(
        90deg,
        rgba(255, 255, 255, 0.001),
        rgb(255, 255, 255) 80%
      );
      content: '';
      height: 44px;
      right: 0;
      pointer-events: none;
      position: absolute;
      top: 0;
      width: 40px;
    }
  }

  .solid-tabs .tabs__item {
    font-size: 18px;
    padding: 12px;
  }

  .title {
    font-size: 16px !important;
  }

  table.table thead th:first-child,
  table.table tbody td:first-child,
  table.table thead th:not(:first-child) {
    padding: 0 12px;
  }
}
</style>
