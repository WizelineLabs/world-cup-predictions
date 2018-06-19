import Team from '@/services/TeamService';

const getTeams = async (context) => {
  const teams = await Team.getTeams();

  // Add Advance Prob
  const teamsWithAdvance = teams.map((team) => {
    const currentTeam = team;
    currentTeam.advance =
      currentTeam.pass_group_runner_prob + currentTeam.pass_group_winner_prob;
    return currentTeam;
  });
  context.commit('setTeams', teamsWithAdvance);
};

const removeTeams = (context) => {
  context.commit('removeTeams');
};

export default {
  getTeams,
  removeTeams,
};
