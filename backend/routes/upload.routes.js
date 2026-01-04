const router = require("express").Router();
const { uploadMedia } = require("../controllers/upload.controller");

router.post("/", uploadMedia);

module.exports = router;
