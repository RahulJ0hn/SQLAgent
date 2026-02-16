const { Router } = require("express");
const router = Router();

// Auth removed — no login required
router.get("/", (_req, res) => {
  res.json({ message: "Authentication not required" });
});

module.exports = router;
