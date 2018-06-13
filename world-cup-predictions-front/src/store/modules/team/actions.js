import Team from '@/services/TeamService';

const getTeams = async (context) => {
  const teams = await Team.getTeams();
  context.commit('setTeams', teams);
};

const removeTeams = (context) => {
  context.commit('removeTeams');
};

export default {
  getTeams,
  removeTeams,
};
