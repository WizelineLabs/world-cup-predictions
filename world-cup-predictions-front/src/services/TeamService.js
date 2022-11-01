import axios from 'axios';

const apiUrl = import.meta.env.API_URL;

export default {
  getTeams() {
    return axios.get(`${apiUrl}/team/`);
  },
};
