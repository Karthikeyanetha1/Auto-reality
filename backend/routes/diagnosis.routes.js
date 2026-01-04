const router = require("express").Router();
const Diagnosis = require("../models/Diagnosis");
const { diagnose } = require("../controllers/diagnosis.controller");

// POST - create diagnosis
router.post("/", diagnose);

// GET - fetch all diagnoses
router.get("/", async (req, res) => {
  const data = await Diagnosis.find().sort({ createdAt: -1 });
  res.json(data);
});

module.exports = router;
