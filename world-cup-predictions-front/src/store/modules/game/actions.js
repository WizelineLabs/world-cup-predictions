import Game from '@/services/GameService';
import User from '../../../services/UserService';

const getGames = async (context) => {
  const games = await Game.getGames();
  const predictions = await Game.getPredictions();
  const votes = await User.getVotes();
  const trends = await Game.getTrends();

  const gamesWithPred = games.map((game) => {
    const pred =
      predictions.find(
        // eslint-disable-next-line
        (prediction) => prediction.game_id === game.id,
      ) || {};
    const guess =
      votes.find(
        // eslint-disable-next-line
        (vote) => vote.game_id === game.id,
      ) || {};
    const trend =
      trends.find(
        // eslint-disable-next-line
        (t) => t.game_id === game.id,
      ) || {};
    return Object.assign(guess, pred, game, trend);
  });

  context.commit('setGames', gamesWithPred);
};

const removeGames = (context) => {
  context.commit('removeGames');
};

export default {
  getGames,
  removeGames,
};
