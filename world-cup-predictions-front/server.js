const history = require('connect-history-api-fallback');
const express = require('express');

const app = express();
app.use(history());

app.use(express.static('dist'));

app.listen(8080, () =>
  console.log('Server listening on: http://localhost:8080'),
);
