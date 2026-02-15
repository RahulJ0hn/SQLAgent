const { Router } = require("express");
const axios = require("axios");
const { config } = require("../config");

const router = Router();

router.post("/", async (req, res) => {
  const { question, session_id } = req.body;

  if (!question || question.trim().length === 0) {
    return res.status(400).json({ error: "Question is required" });
  }

  try {
    const response = await axios.post(
      `${config.agentUrl}/api/v1/query`,
      { question, session_id },
      { timeout: 120000 }
    );

    res.json(response.data);
  } catch (error) {
    if (error.response) {
      res.status(error.response.status).json(error.response.data);
    } else {
      res.status(500).json({ error: "Agent service unavailable" });
    }
  }
});

module.exports = router;
