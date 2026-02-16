import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "/api",
  headers: { "Content-Type": "application/json" },
  timeout: 120000, // 2 min timeout for Render free tier cold starts
});

export async function sendQuery(question, retries = 2) {
  for (let i = 0; i <= retries; i++) {
    try {
      const { data } = await api.post("/query", { question });
      return data;
    } catch (err) {
      const status = err.response?.status;
      if ((status === 502 || status === 503) && i < retries) {
        // Render is waking up, wait and retry
        await new Promise((r) => setTimeout(r, 5000));
        continue;
      }
      throw err;
    }
  }
}

export default api;
