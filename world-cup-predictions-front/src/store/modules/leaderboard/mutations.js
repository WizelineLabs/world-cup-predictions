const setLeaderboard = (state, list) => {
  state.list = list;
};

const removeLeaderboard = (state) => {
  state.list = [];
};

const setMyLeaderboard = (state, list) => {
  state.myList = list;
};

const removeMyLeaderboard = (state) => {
  state.myList = [];
};

export default {
  setLeaderboard,
  removeLeaderboard,
  setMyLeaderboard,
  removeMyLeaderboard,
};
