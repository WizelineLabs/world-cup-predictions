const setGames = (state, games) => {
  state.list = games;
};

const removeGames = (state) => {
  state.list = [];
};

export default {
  setGames,
  removeGames,
};
