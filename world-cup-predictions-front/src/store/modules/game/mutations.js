const setGames = (state, games) => {
  state.games = games;
};

const removeGames = (state) => {
  state.games = [];
};

export default {
  setGames,
  removeGames,
};
