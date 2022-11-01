import axios from 'axios';

const API_URL = import.meta.env.API_URL;
const WCP_TOKEN = 'wcp-token';

export default {
  login(data) {
    const form = new FormData();
    form.append('access_token', data.access_token);

    const settings = {
      url: `${API_URL}/social/google-oauth2/`,
      method: 'POST',
      mimeType: 'multipart/form-data',
      data: form,
    };

    return axios(settings);
  },

  logout() {
    const token = localStorage.getItem(WCP_TOKEN);

    const settings = {
      url: `${API_URL}/logout/`,
      method: 'GET',
      headers: {
        Authorization: `Token ${token}`,
      },
    };

    return axios(settings);
  },
};
