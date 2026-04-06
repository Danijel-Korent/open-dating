/**
 * @param {string} path Query string after backend/api.php — e.g. "action=feed"
 */
function apiUrl(path) {
  const base = typeof window !== "undefined" && window.__API_BASE__ ? window.__API_BASE__ : "";
  return base + "backend/api.php?" + path;
}

/**
 * @param {string} path
 * @param {object} [opts]
 */
async function apiGet(path, opts) {
  const r = await fetch(apiUrl(path), {
    credentials: "include",
    ...opts,
  });
  const text = await r.text();
  let data;
  try {
    data = text ? JSON.parse(text) : {};
  } catch {
    throw new Error("Invalid JSON from API");
  }
  if (!r.ok) {
    throw new Error(data.error || r.statusText || "Request failed");
  }
  return data;
}

/**
 * @param {string} path
 * @param {object} body
 */
async function apiPost(path, body) {
  const r = await fetch(apiUrl(path), {
    method: "POST",
    credentials: "include",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const text = await r.text();
  let data;
  try {
    data = text ? JSON.parse(text) : {};
  } catch {
    throw new Error("Invalid JSON from API");
  }
  if (!r.ok) {
    throw new Error(data.error || r.statusText || "Request failed");
  }
  return data;
}

window.apiGet = apiGet;
window.apiPost = apiPost;
window.apiUrl = apiUrl;
