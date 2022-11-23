const setLeaderboard = (state, list) => {
  state.leaderboard.list = list;
};

const removeLeaderboard = (state) => {
  state.leaderboard.list = [];
};

const setMyLeaderboard = (state, list) => {
  state.leaderboard.myList = list;
};

const removeMyLeaderboard = (state) => {
  state.leaderboard.myList = [];
};

export default {
  setLeaderboard,
  removeLeaderboard,
  setMyLeaderboard,
  removeMyLeaderboard,
};
