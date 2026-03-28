const API_URL = process.env.EXPO_PUBLIC_API_URL || "http://localhost:8000/api/v1";

async function request(path, options = {}, token) {
  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(options.headers || {})
    }
  });

  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(data.detail || data.message || "Request failed");
  }
  return data;
}

export const api = {
  signup: (payload) => request("/auth/signup", { method: "POST", body: JSON.stringify(payload) }),
  login: (payload) => request("/auth/login", { method: "POST", body: JSON.stringify(payload) }),
  me: (token) => request("/auth/me", {}, token),
  updateRiskLimit: (value, token) => request(`/auth/risk-limit?max_trade_size=${value}`, { method: "PATCH" }, token),
  connectCoinSwitch: (payload, token) => request("/coinswitch/connect", { method: "POST", body: JSON.stringify(payload) }, token),
  coinSwitchStatus: (token) => request("/coinswitch/status", {}, token),
  dashboard: (token) => request("/dashboard/summary", {}, token),
  trades: (token) => request("/dashboard/trades", {}, token),
  signalHistory: (token) => request("/signals/history", {}, token),
  createSignal: (payload, token) => request("/signals/manual", { method: "POST", body: JSON.stringify(payload) }, token)
};
