import axios from 'axios';

const apiUrl = process.env.API_URL;

export default {
  getTeams() {
    return axios.get(`${apiUrl}/team/`);
  },
};
