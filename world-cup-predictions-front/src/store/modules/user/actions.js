import Auth from '@/services/AuthService';
import User from '@/services/UserService';

const USER = 'user';
const WCP_TOKEN = 'wcp-token';

// eslint-disable-next-line
const loginUser = (context, data) => {
  return new Promise((resolve, reject) => {
    Auth.login(data)
      .then((response) => {
        const token = response.token;
        localStorage.setItem(WCP_TOKEN, token);
        context.commit('setToken', token);
        resolve(response);
      })
      .catch((err) => {
        localStorage.removeItem(WCP_TOKEN);
        context.commit('removeToken');
        reject(err);
      });
  });
};

const logoutUser = (context) => {
  Auth.logout().then(() => {
    localStorage.removeItem(WCP_TOKEN);
    localStorage.removeItem(USER);
    context.commit('removeToken');
    context.commit('removeUser');
  });
};

// eslint-disable-next-line
const getUser = (context) => {
  return new Promise((resolve, reject) => {
    User.getUser()
      .then((response) => {
        const user = response.length ? response[0] : {};

        localStorage.setItem(USER, JSON.stringify(user));
        context.commit('setUser', user);
        resolve(user);
      })
      .catch((err) => {
        localStorage.removeItem(USER);
        context.commit('removeUser');
        localStorage.removeItem(WCP_TOKEN);
        context.commit('removeToken');
        reject(err);
      });
  });
};

// eslint-disable-next-line
const fetchLocalUser = (context) => {
  return new Promise((resolve) => {
    const localUser = JSON.parse(localStorage.getItem(USER));
    context.commit('setUser', localUser);
    resolve(localUser);
  });
};

const setLoginMessage = (context, data) => {
  context.commit('setLoginMessage', data);
};

const toogleLoading = (context) => {
  context.commit('toogleLoading');
};

const setWildcard = async (context, data) => {
  const wildcard = await User.setWildcard(data.wildcardId);
  return wildcard;
};

const setGuess = async (context, data) => {
  const guess = await User.setGuess(data.game_id, data.choice);
  return guess;
};

export default {
  loginUser,
  getUser,
  logoutUser,
  fetchLocalUser,
  setLoginMessage,
  toogleLoading,
  setWildcard,
  setGuess,
};
