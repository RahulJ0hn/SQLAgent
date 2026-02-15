const { Queue } = require("bullmq");
const IORedis = require("ioredis");
const { config } = require("../config");

let connection = null;
let queryQueue = null;

function initQueue() {
  connection = new IORedis(config.redisUrl, { maxRetriesPerRequest: null });
  queryQueue = new Queue("sql-queries", { connection });
  console.log("BullMQ query queue initialized");
  return queryQueue;
}

function getQueue() {
  return queryQueue;
}

module.exports = { initQueue, getQueue };
