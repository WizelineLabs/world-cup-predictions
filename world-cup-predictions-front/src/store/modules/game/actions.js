import Game from '@/services/GameService';
import User from '../../../services/UserService';

const getGames = async (context) => {
  Promise.all([Game.getGames(), Game.getPredictions(), User.getVotes(), Game.getTrends()]).then((values) => {
    const games = values[0];
    const predictions = values[1];
    const votes = values[2];
    const trends = values[3];

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
          (t) => t.id === game.id,
        ) || {};
      return Object.assign(guess, pred, game, trend);
    });
  
    context.commit('setGames', gamesWithPred);
  }).catch(err => {
    console.error(err)
  });
};

const removeGames = (context) => {
  context.commit('removeGames');
};

export default {
  getGames,
  removeGames,
};
