import axios from "axios";

const API = axios.create({
  baseURL: "https://railguard-ai-powered-indian-railway-v838.onrender.com/api",
});

export default API;