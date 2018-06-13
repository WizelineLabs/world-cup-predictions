const setUser = (state, user) => {
  state.data = user;
};

const removeUser = (state) => {
  state.data = {};
};

const setToken = (state, token) => {
  state.token = token;
};

const removeToken = (state) => {
  state.token = null;
};

const setLoginMessage = (state, message) => {
  state.loginMessage = message;
};

const toogleLoading = (state) => {
  state.loginLoading = !state.loginLoading;
};

export default {
  setUser,
  removeUser,
  setToken,
  removeToken,
  setLoginMessage,
  toogleLoading,
};
