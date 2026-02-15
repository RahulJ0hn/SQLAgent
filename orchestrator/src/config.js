require("dotenv").config();

const config = {
  port: parseInt(process.env.ORCHESTRATOR_PORT || "3000"),
  agentUrl: process.env.AGENT_URL || "http://localhost:8080",
  redisUrl: process.env.REDIS_URL || "redis://localhost:6379",
  jwtSecret: process.env.JWT_SECRET || "change-me-in-production",
  jwtExpiresIn: "24h",
};

module.exports = { config };
