const { Router } = require("express");
const { v4: uuidv4 } = require("uuid");

const router = Router();
const sessions = new Map();

router.post("/", (req, res) => {
  const session = {
    id: uuidv4(),
    queries: [],
    createdAt: new Date().toISOString(),
  };
  sessions.set(session.id, session);
  res.status(201).json(session);
});

router.get("/", (_req, res) => {
  res.json(Array.from(sessions.values()));
});

router.get("/:id", (req, res) => {
  const session = sessions.get(req.params.id);
  if (!session) return res.status(404).json({ error: "Session not found" });
  res.json(session);
});

router.delete("/:id", (req, res) => {
  if (!sessions.has(req.params.id)) return res.status(404).json({ error: "Session not found" });
  sessions.delete(req.params.id);
  res.status(204).send();
});

module.exports = router;
