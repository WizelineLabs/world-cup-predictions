import axios from 'axios';

const API_URL = import.meta.env.API_URL;
const WCP_TOKEN = 'wcp-token';

export default {
  getUser() {
    const token = localStorage.getItem(WCP_TOKEN);

    const settings = {
      url: `${API_URL}/user/`,
      method: 'GET',
      headers: {
        Authorization: `Token ${token}`,
      },
    };

    return axios(settings);
  },

  setWildcard(wildcardId) {
    const token = localStorage.getItem(WCP_TOKEN);

    const settings = {
      url: `${API_URL}/wildcard/`,
      method: 'POST',
      headers: {
        Authorization: `Token ${token}`,
      },
      data: {
        wildcard: parseInt(wildcardId, 10),
      },
    };

    return axios(settings);
  },

  getVotes() {
    const token = localStorage.getItem(WCP_TOKEN);

    const settings = {
      url: `${API_URL}/vote/`,
      method: 'GET',
      headers: {
        Authorization: `Token ${token}`,
      },
    };

    return axios(settings);
  },

  setGuess(gameId, choice) {
    const token = localStorage.getItem(WCP_TOKEN);

    const settings = {
      url: `${API_URL}/guess/`,
      method: 'POST',
      headers: {
        Authorization: `Token ${token}`,
      },
      data: {
        game_id: parseInt(gameId, 10),
        choice,
      },
    };

    return axios(settings);
  },

  isAuthenticated() {
    const token = localStorage.getItem(WCP_TOKEN);
    return !!token;
  },
};
