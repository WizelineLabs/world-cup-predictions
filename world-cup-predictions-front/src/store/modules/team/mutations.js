const setTeams = (state, teams) => {
  state.teams = teams;
};

const removeTeams = (state) => {
  state.teams = [];
};

export default {
  setTeams,
  removeTeams,
};
