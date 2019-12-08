// server.js
const express = require("express");
const app = express();

app.set("views", "views");
app.set("view engine", "pug");

app.get("/", function(req, res) {
   res.render("hello");
});

app.listen(3000, () => {
  console.log('Visit http://localhost:3000/ to see this example');
});