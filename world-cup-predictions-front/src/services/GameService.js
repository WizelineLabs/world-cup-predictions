import axios from 'axios';

const API_URL = process.env.API_URL;
const WCP_TOKEN = 'wcp-token';

export default {
  getGames() {
    const token = localStorage.getItem(WCP_TOKEN);

    const settings = {
      url: `${API_URL}/game/`,
      method: 'GET',
      headers: {
        Authorization: `Token ${token}`,
      },
    };

    return axios(settings);
  },

  getPredictions() {
    const token = localStorage.getItem(WCP_TOKEN);

    const settings = {
      url: `${API_URL}/prediction/`,
      method: 'GET',
      headers: {
        Authorization: `Token ${token}`,
      },
    };

    return axios(settings);
  },
};
