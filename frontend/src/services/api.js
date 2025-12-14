const API_URL = "http://127.0.0.1:8000/api";

// -------------------------
// Refresh Token Handler
// -------------------------
async function refreshToken() {
  const refresh = localStorage.getItem("refresh_token");
  if (!refresh) throw new Error("No refresh token available");

  const res = await fetch(`${API_URL}/token/refresh/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ refresh }),
  });

  const data = await res.json();

  if (res.ok && data.access) {
    localStorage.setItem("access_token", data.access);
    return data.access;
  } else {
    throw new Error(data.detail || "Failed to refresh token");
  }
}

// -------------------------
// Global Fetch Wrapper
// -------------------------
export async function apiFetch(endpoint, options = {}) {
  let token = localStorage.getItem("access_token");

  // Attach Authorization header
  const headers = {
    "Content-Type": "application/json",
    ...(options.headers || {}),
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };

  let res = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers,
    credentials: "include",
  });

  // If token expired → refresh and retry
  if (res.status === 401) {
    try {
      token = await refreshToken();
      const retryHeaders = {
        ...headers,
        Authorization: `Bearer ${token}`,
      };

      res = await fetch(`${API_URL}${endpoint}`, {
        ...options,
        headers: retryHeaders,
        credentials: "include",
      });
    } catch (err) {
      throw new Error("Session expired. Please log in again.");
    }
  }

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || "Request failed");
  }

  return res.json();
}

// -------------------------
// Example API Functions
// -------------------------
export function getBooks() {
  return apiFetch("/books/", { method: "GET" });
}

export function addBook(bookData) {
  return apiFetch("/books/", {
    method: "POST",
    body: JSON.stringify(bookData),
  });
}

export function login(username, password) {
  return fetch(`${API_URL}/token/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.access) {
        localStorage.setItem("access_token", data.access);
        localStorage.setItem("refresh_token", data.refresh);
        return data.access;
      } else {
        throw new Error(data.detail || "Login failed");
      }
    });
}

export function logout() {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
}
