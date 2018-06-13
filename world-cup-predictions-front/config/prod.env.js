require('dotenv').config()

module.exports = {
  NODE_ENV: '"production"',
  API_URL: `"${process.env.API_URL}"`,
  GOOGLE_AUTH_KEY: `"${process.env.GOOGLE_AUTH_KEY}"`
};
