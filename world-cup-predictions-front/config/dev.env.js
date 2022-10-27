'use strict'
const { merge } = require('webpack-merge');
const prodEnv = require('./prod.env')
require('dotenv').config()

module.exports = merge(prodEnv, {
  NODE_ENV: '"development"',
  API_URL: `"${process.env.API_URL}"`,
  GOOGLE_AUTH_KEY: `"${process.env.GOOGLE_AUTH_KEY}"`
})
