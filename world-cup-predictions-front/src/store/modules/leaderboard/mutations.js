const setLeaderboard = (state, list) => {
  state.list = list;
};

const removeLeaderboard = (state) => {
  state.list = [];
};

export default {
  setLeaderboard,
  removeLeaderboard,
};
