const multer = require("multer");
const multerS3 = require("multer-s3");
const s3 = require("../config/cloud");

const upload = multer({
  storage: multerS3({
    s3,
    bucket: process.env.AWS_BUCKET,
    acl: "public-read",
    key: (req, file, cb) => {
      cb(null, `uploads/${Date.now()}-${file.originalname}`);
    }
  })
});

module.exports = upload;
