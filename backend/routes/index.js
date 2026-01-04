const express = require("express");
const router = express.Router();

const uploadRoutes = require("./upload.routes");
const diagnosisRoutes = require("./diagnosis.routes");

router.use("/upload", uploadRoutes);
router.use("/diagnosis", diagnosisRoutes);

module.exports = router;
