const { Router } = require("express");
const { v4: uuidv4 } = require("uuid");
const { authMiddleware } = require("../middleware/auth");

const router = Router();

// In-memory session store (replace with Redis in production)
const sessions = new Map();

router.use(authMiddleware);

router.post("/", (req, res) => {
  const session = {
    id: uuidv4(),
    userId: req.user.userId,
    queries: [],
    createdAt: new Date().toISOString(),
  };
  sessions.set(session.id, session);
  res.status(201).json(session);
});

router.get("/", (req, res) => {
  const userSessions = Array.from(sessions.values()).filter(
    (s) => s.userId === req.user.userId
  );
  res.json(userSessions);
});

router.get("/:id", (req, res) => {
  const session = sessions.get(req.params.id);
  if (!session || session.userId !== req.user.userId) {
    return res.status(404).json({ error: "Session not found" });
  }
  res.json(session);
});

router.delete("/:id", (req, res) => {
  const session = sessions.get(req.params.id);
  if (!session || session.userId !== req.user.userId) {
    return res.status(404).json({ error: "Session not found" });
  }
  sessions.delete(req.params.id);
  res.status(204).send();
});

module.exports = router;
