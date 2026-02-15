const IORedis = require("ioredis");
const { config } = require("../config");

let redis = null;

function initSessionStore() {
  redis = new IORedis(config.redisUrl);
  console.log("Redis session store initialized");
}

async function saveSession(session) {
  if (!redis) return;
  await redis.set(
    `session:${session.id}`,
    JSON.stringify(session),
    "EX",
    86400 // 24 hour TTL
  );
}

async function getSession(id) {
  if (!redis) return null;
  const data = await redis.get(`session:${id}`);
  return data ? JSON.parse(data) : null;
}

async function deleteSession(id) {
  if (!redis) return;
  await redis.del(`session:${id}`);
}

module.exports = { initSessionStore, saveSession, getSession, deleteSession };
