const Diagnosis = require("../models/Diagnosis");
const { runDiagnosis } = require("../services/ai.service");

exports.diagnose = async (req, res) => {
  const aiResult = await runDiagnosis(req.body);

  const record = await Diagnosis.create({
    userId: req.user?.uid || "anonymous",
    machine: req.body.machine,
    inputs: req.body.inputs,
    result: aiResult.result,
    confidence: aiResult.confidence
  });

  res.json(record);
};
