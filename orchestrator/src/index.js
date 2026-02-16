const express = require("express");
const cors = require("cors");
const { config } = require("./config");
const { rateLimiter } = require("./middleware/rateLimiter");
const authRoutes = require("./routes/auth");
const queryRoutes = require("./routes/query");
const sessionRoutes = require("./routes/sessions");

const app = express();

// Middleware
const allowedOrigins = [
  "http://localhost:5173",
  "http://localhost:3000",
  process.env.CLIENT_URL,
].filter(Boolean);
app.use(cors({
  origin: (origin, callback) => {
    // Allow requests with no origin (mobile apps, curl, etc.)
    if (!origin) return callback(null, true);
    // Allow configured origins and any Vercel preview URLs
    if (allowedOrigins.includes(origin) || origin.endsWith(".vercel.app")) {
      return callback(null, true);
    }
    callback(new Error("Not allowed by CORS"));
  },
  credentials: true,
}));
app.use(express.json());
app.use(rateLimiter);

// Routes
app.use("/api/auth", authRoutes);
app.use("/api/query", queryRoutes);
app.use("/api/sessions", sessionRoutes);

// Health check
app.get("/api/health", (_req, res) => {
  res.json({ status: "healthy", service: "orchestrator" });
});

// Global error handler
app.use((err, req, res, _next) => {
  console.error("Unhandled error:", err);
  res.status(500).json({ error: "Internal server error", details: err.message });
});

app.listen(config.port, () => {
  console.log(`Orchestrator running on port ${config.port}`);
  console.log(`Agent URL: ${config.agentUrl}`);
});
