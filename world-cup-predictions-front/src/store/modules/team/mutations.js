const setTeams = (state, teams) => {
  state.list = teams;
};

const removeTeams = (state) => {
  state.list = [];
};

export default {
  setTeams,
  removeTeams,
};
