import axios from 'axios';

const apiUrl = import.meta.env.VITE_API_URL;

export default {
  getTeams() {
    return axios.get(`${apiUrl}/team/`);
  },
};
