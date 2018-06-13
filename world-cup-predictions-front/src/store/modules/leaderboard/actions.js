import Leaderboard from '@/services/LeaderboardService';

const getLeaderboard = async (context) => {
  const leaderboard = await Leaderboard.getLeaderboard();
  context.commit('setLeaderboard', leaderboard);
};

const removeLeaderboard = (context) => {
  context.commit('removeLeaderboard');
};

export default {
  getLeaderboard,
  removeLeaderboard,
};
