/**
 * HTTP helpers for `backend/api.php`. `window.__API_BASE__` (if set) is prepended for subdirectory deploys.
 */

/**
 * Build the full URL for an API request.
 *
 * @param {string} path Query string after `backend/api.php` (e.g. `"action=feed"`).
 * @returns {string}
 */
function apiUrl(path) {
  const base = typeof window !== "undefined" && window.__API_BASE__ ? window.__API_BASE__ : "";
  return base + "backend/api.php?" + path;
}

/**
 * GET JSON from the API (cookies included). Throws if the response is not OK or body is not JSON.
 *
 * @param {string} path
 * @param {RequestInit} [opts] Extra `fetch` options (merged with credentials).
 * @returns {Promise<any>}
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
 * POST JSON to the API (cookies included). Throws if the response is not OK or body is not JSON.
 *
 * @param {string} path
 * @param {object} body
 * @returns {Promise<any>}
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
