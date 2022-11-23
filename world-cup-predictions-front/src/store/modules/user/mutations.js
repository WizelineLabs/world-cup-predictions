const setUser = (state, user) => {
  state.user.data = user;
};

const removeUser = (state) => {
  state.user = {};
};

const setToken = (state, token) => {
  state.token = token;
};

const removeToken = (state) => {
  state.token = null;
};

const setLoginMessage = (state, message) => {
  state.user.loginMessage = message;
};

const toogleLoading = (state) => {
  state.user.loginLoading = !state.user.loginLoading;
};

export default {
  setUser,
  removeUser,
  setToken,
  removeToken,
  setLoginMessage,
  toogleLoading,
};
