import axios from 'axios';

const API_URL = import.meta.env.API_URL;
const WCP_TOKEN = 'wcp-token';

export default {
  getLeaderboard() {
    const token = localStorage.getItem(WCP_TOKEN);

    const settings = {
      url: `${API_URL}/leaderboard/`,
      method: 'GET',
      headers: {
        Authorization: `Token ${token}`,
      },
    };

    return axios(settings);
  },
  getMyLeaderboard() {
    const token = localStorage.getItem(WCP_TOKEN);

    const settings = {
      url: `${API_URL}/myleaderboard/`,
      method: 'GET',
      headers: {
        Authorization: `Token ${token}`,
      },
    };

    return axios(settings);
  },
  follow(userId) {
    const token = localStorage.getItem(WCP_TOKEN);

    const settings = {
      url: `${API_URL}/follow/add/`,
      method: 'POST',
      headers: {
        Authorization: `Token ${token}`,
      },
      data: {
        user_id: parseInt(userId, 10),
      },
    };

    return axios(settings);
  },
  unfollow(userId) {
    const token = localStorage.getItem(WCP_TOKEN);

    const settings = {
      url: `${API_URL}/follow/remove/`,
      method: 'POST',
      headers: {
        Authorization: `Token ${token}`,
      },
      data: {
        user_id: parseInt(userId, 10),
      },
    };

    return axios(settings);
  },
  unfollowAll() {
    const token = localStorage.getItem(WCP_TOKEN);

    const settings = {
      url: `${API_URL}/follow/reset/`,
      method: 'POST',
      headers: {
        Authorization: `Token ${token}`,
      },
    };

    return axios(settings);
  },
};
