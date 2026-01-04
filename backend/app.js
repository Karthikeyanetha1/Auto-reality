require("dotenv").config();
const express = require("express");
const cors = require("cors");

const connectDB = require("./config/db");
const routes = require("./routes");

const app = express();

connectDB();

app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.use("/api", routes);

app.get("/", (req, res) => {
  res.send("AutoFix Reality Backend Running");
});

module.exports = app;
