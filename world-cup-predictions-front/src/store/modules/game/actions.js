import Game from '@/services/GameService';
import User from '../../../services/UserService';

const getGames = async (context) => {
  const games = await Game.getGames();
  const predictions = await Game.getPredictions();
  const votes = await User.getVotes();

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
    return Object.assign(guess, pred, game);
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