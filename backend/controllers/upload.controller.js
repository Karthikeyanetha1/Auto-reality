exports.uploadMedia = (req, res) => {
  res.json({
    message: "Upload successful",
    files: req.files || req.file
  });
};
