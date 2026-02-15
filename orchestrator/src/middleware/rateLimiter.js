const requestCounts = new Map();

const WINDOW_MS = 60000; // 1 minute
const MAX_REQUESTS = 30;

function rateLimiter(req, res, next) {
  const key = req.ip || "unknown";
  const now = Date.now();

  const entry = requestCounts.get(key);

  if (!entry || now > entry.resetAt) {
    requestCounts.set(key, { count: 1, resetAt: now + WINDOW_MS });
    return next();
  }

  if (entry.count >= MAX_REQUESTS) {
    return res.status(429).json({ error: "Too many requests. Please try again later." });
  }

  entry.count++;
  next();
}

module.exports = { rateLimiter };
