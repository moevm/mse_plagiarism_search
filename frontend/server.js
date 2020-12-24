var express = require('express');
var history = require('connect-history-api-fallback');
var app = express();

const port = process.env.PORT ?? 8080;
const staticFileMiddleware = express.static('dist');

app.use(staticFileMiddleware);

app.use(history());

app.use(staticFileMiddleware);

app.listen(port, function () {
  console.log(`App listening on port ${port}!`);
});
