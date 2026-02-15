import axios from "axios";

const api = axios.create({
  baseURL: "/api",
  headers: { "Content-Type": "application/json" },
});

export async function sendQuery(question) {
  const { data } = await api.post("/query", { question });
  return data;
}

export default api;
