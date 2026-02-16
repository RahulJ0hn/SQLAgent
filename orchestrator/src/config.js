require("dotenv").config();

// REDIS_URL or REDIS_HOST+REDIS_PORT (e.g. Render fromService)
const redisUrl =
  process.env.REDIS_URL ||
  (process.env.REDIS_HOST && process.env.REDIS_PORT
    ? `redis://${process.env.REDIS_HOST}:${process.env.REDIS_PORT}`
    : "redis://localhost:6379");

const config = {
  port: parseInt(process.env.PORT || process.env.ORCHESTRATOR_PORT || "3000"),
  agentUrl: process.env.AGENT_URL || "http://localhost:8080",
  redisUrl,
  jwtSecret: process.env.JWT_SECRET || "change-me-in-production",
  jwtExpiresIn: "24h",
};

module.exports = { config };
