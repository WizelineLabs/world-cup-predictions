import Leaderboard from '@/services/LeaderboardService';

const getLeaderboard = async (context) => {
  const leaderboard = await Leaderboard.getLeaderboard();
  context.commit('setLeaderboard', leaderboard);
};

const removeLeaderboard = (context) => {
  context.commit('removeLeaderboard');
};

const getMyLeaderboard = async (context) => {
  const leaderboard = await Leaderboard.getMyLeaderboard();
  context.commit('setMyLeaderboard', leaderboard);
};

const removeMyLeaderboard = (context) => {
  context.commit('removeMyLeaderboard');
};

const follow = async (context, data) => {
  const user = await Leaderboard.follow(data.user_id);
  return user;
};

const unfollow = async (context, data) => {
  const user = await Leaderboard.unfollow(data.user_id);
  return user;
};

const unfollowAll = async () => {
  const user = await Leaderboard.unfollowAll();
  return user;
};

export default {
  getLeaderboard,
  removeLeaderboard,
  getMyLeaderboard,
  removeMyLeaderboard,
  follow,
  unfollow,
  unfollowAll,
};
