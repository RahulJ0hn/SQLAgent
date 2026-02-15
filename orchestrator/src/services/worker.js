const { Worker } = require("bullmq");
const IORedis = require("ioredis");
const axios = require("axios");
const { config } = require("../config");

function startWorker() {
  const connection = new IORedis(config.redisUrl, {
    maxRetriesPerRequest: null,
  });

  const worker = new Worker(
    "sql-queries",
    async (job) => {
      const { question, session_id } = job.data;
      const response = await axios.post(`${config.agentUrl}/api/v1/query`, {
        question,
        session_id,
      });
      return response.data;
    },
    { connection, concurrency: 5 }
  );

  worker.on("completed", (job) => {
    console.log(`Job ${job.id} completed`);
  });

  worker.on("failed", (job, err) => {
    console.error(`Job ${job?.id} failed:`, err.message);
  });

  console.log("BullMQ worker started");
  return worker;
}

module.exports = { startWorker };
