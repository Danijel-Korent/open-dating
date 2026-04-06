/* global apiGet, apiPost */

function escapeHtml(s) {
  const d = document.createElement("div");
  d.textContent = s;
  return d.innerHTML;
}

function parseHash() {
  const h = (location.hash || "#/feed").replace(/^#/, "") || "/feed";
  const parts = h.split("/").filter(Boolean);
  const route = parts[0] || "feed";
  const arg = parts[1] ? decodeURIComponent(parts[1]) : null;
  return { route, arg, raw: h };
}

const state = {
  session: null,
  feedUser: null,
  error: null,
};

async function loadSession() {
  state.session = await apiGet("action=session");
}

function navItems() {
  return [
    { id: "feed", label: "Discover", icon: "◇" },
    { id: "likes", label: "Likes", icon: "♡" },
    { id: "matches", label: "Matches", icon: "✦" },
    { id: "chats", label: "Chats", icon: "💬" },
    { id: "profile", label: "Profile", icon: "☺" },
  ];
}

function renderNav(active) {
  const items = navItems();
  return `
    <nav class="bottom-nav" role="navigation" aria-label="Main">
      ${items
        .map(
          (it) => `
        <a href="#/${it.id}" class="bottom-nav__btn ${it.id === active ? "is-active" : ""}" data-route="${escapeHtml(it.id)}">
          <span class="bottom-nav__icon" aria-hidden="true">${it.icon}</span>
          <span class="bottom-nav__label">${escapeHtml(it.label)}</span>
        </a>`
        )
        .join("")}
    </nav>`;
}

function renderHeader(title, subtitle) {
  return `
    <header class="app-header">
      <h1 class="app-header__title">${escapeHtml(title)}</h1>
      ${subtitle ? `<p class="app-header__sub">${escapeHtml(subtitle)}</p>` : ""}
    </header>`;
}

async function viewFeed() {
  let data;
  try {
    data = await apiGet("action=feed");
  } catch (e) {
    return renderHeader("Discover", "") + `<p class="banner banner--error">${escapeHtml(String(e.message))}</p>`;
  }
  const u = data.user;
  state.feedUser = u;
  if (!u) {
    return (
      renderHeader("Discover", "No more profiles right now") +
      `<div class="empty-card"><p>Check back later or adjust your preferences.</p></div>`
    );
  }
  const pics = u.picture_urls || [];
  const hero = pics[0] || "";
  const interests = (u.interests || []).map((x) => x.name || x.id).join(" · ");
  return `
    ${renderHeader("Discover", "")}
    <article class="profile-card">
      <div class="profile-card__photo-wrap">
        ${hero ? `<img class="profile-card__photo" src="${escapeHtml(hero)}" alt="" width="400" height="520" loading="lazy">` : `<div class="profile-card__photo profile-card__photo--empty">No photo</div>`}
      </div>
      <div class="profile-card__body">
        <h2 class="profile-card__name">${escapeHtml(u.name)}, ${u.age}</h2>
        <p class="profile-card__meta">${escapeHtml(u.location || "")}</p>
        <p class="profile-card__bio">${escapeHtml(u.bio || "")}</p>
        ${interests ? `<p class="profile-card__tags">${escapeHtml(interests)}</p>` : ""}
      </div>
      <div class="profile-card__actions">
        <button type="button" class="btn btn--pass" data-react="pass" data-user="${escapeHtml(u.username)}">Pass</button>
        <button type="button" class="btn btn--like" data-react="like" data-user="${escapeHtml(u.username)}">Like</button>
      </div>
    </article>`;
}

async function viewLikes() {
  let data;
  try {
    data = await apiGet("action=likes");
  } catch (e) {
    return renderHeader("Likes you", "") + `<p class="banner banner--error">${escapeHtml(String(e.message))}</p>`;
  }
  const users = data.users || [];
  if (!users.length) {
    return renderHeader("Likes you", "") + `<div class="empty-card"><p>No one has liked you yet.</p></div>`;
  }
  return (
    renderHeader("Likes you", "They liked you first") +
    `<ul class="user-list">${users.map((u) => userListItemHtml(u, false)).join("")}</ul>`
  );
}

function userListItemHtml(u, showChat) {
  const pic = (u.picture_urls && u.picture_urls[0]) || "";
  return `
    <li class="user-row">
      <a href="#/user/${encodeURIComponent(u.username)}" class="user-row__main">
        <span class="user-row__avatar">${pic ? `<img src="${escapeHtml(pic)}" alt="">` : `<span class="user-row__ph"></span>`}</span>
        <span class="user-row__text">
          <span class="user-row__name">${escapeHtml(u.name)}</span>
          <span class="user-row__meta">${escapeHtml(u.location || "")}</span>
        </span>
      </a>
      ${
        showChat
          ? `<a class="user-row__chat btn btn--small" href="#/chat/${encodeURIComponent(u.username)}">Chat</a>`
          : ""
      }
    </li>`;
}

async function viewMatches() {
  let data;
  try {
    data = await apiGet("action=matches");
  } catch (e) {
    return renderHeader("Matches", "") + `<p class="banner banner--error">${escapeHtml(String(e.message))}</p>`;
  }
  const users = data.users || [];
  if (!users.length) {
    return renderHeader("Matches", "") + `<div class="empty-card"><p>When you both like each other, they show up here.</p></div>`;
  }
  return (
    renderHeader("Matches", "") +
    `<ul class="user-list">${users.map((u) => userListItemHtml(u, true)).join("")}</ul>`
  );
}

async function viewChats() {
  let data;
  try {
    data = await apiGet("action=chats");
  } catch (e) {
    return renderHeader("Chats", "") + `<p class="banner banner--error">${escapeHtml(String(e.message))}</p>`;
  }
  const chats = data.chats || [];
  if (!chats.length) {
    return renderHeader("Chats", "") + `<div class="empty-card"><p>No conversations yet. Get a match first.</p></div>`;
  }
  return (
    renderHeader("Chats", "") +
    `<ul class="chat-list">${chats
      .map((row) => {
        const u = row.user;
        const pic = (u.picture_urls && u.picture_urls[0]) || "";
        const last = row.last_message;
        const preview = last ? last.message : "Say hi…";
        return `
        <li class="chat-row">
          <a href="#/chat/${encodeURIComponent(u.username)}" class="chat-row__link">
            <span class="chat-row__avatar">${pic ? `<img src="${escapeHtml(pic)}" alt="">` : `<span class="user-row__ph"></span>`}</span>
            <span class="chat-row__body">
              <span class="chat-row__name">${escapeHtml(u.name)}</span>
              <span class="chat-row__preview">${escapeHtml(preview)}</span>
            </span>
          </a>
        </li>`;
      })
      .join("")}</ul>`
  );
}

async function viewChat(username) {
  let messages;
  try {
    const data = await apiGet("action=chat_messages&with=" + encodeURIComponent(username));
    messages = data.messages || [];
  } catch (e) {
    return renderHeader("Chat", username) + `<p class="banner banner--error">${escapeHtml(String(e.message))}</p>`;
  }
  let peer = null;
  try {
    const udata = await apiGet("action=user&username=" + encodeURIComponent(username));
    peer = udata.user;
  } catch {
    peer = { name: username, username };
  }
  const title = peer ? peer.name : username;
  const bubbles = messages
    .map((m) => {
      const mine = m.sender_id === state.session.username;
      return `<div class="msg ${mine ? "msg--mine" : "msg--them"}"><div class="msg__bubble">${escapeHtml(m.message)}</div></div>`;
    })
    .join("");
  return `
    ${renderHeader(title, "")}
    <div class="chat-wrap">
      <a href="#/chats" class="back-link">← Chats</a>
      <div class="chat-log" id="chat-log">${bubbles}</div>
      <form class="chat-compose" id="chat-form" data-with="${escapeHtml(username)}">
        <label class="sr-only" for="chat-input">Message</label>
        <input type="text" id="chat-input" name="message" autocomplete="off" placeholder="Message…" class="chat-input">
        <button type="submit" class="btn btn--send">Send</button>
      </form>
    </div>`;
}

async function viewProfile() {
  const u = state.session.user;
  const prefs = u.preferences;
  const g = prefs.gender;
  const usersList = await apiGet("action=users");
  const all = usersList.users || [];
  const options = all
    .concat([u])
    .filter((x, i, arr) => arr.findIndex((y) => y.username === x.username) === i)
    .sort((a, b) => a.name.localeCompare(b.name));
  return `
    ${renderHeader("Profile", u.name)}
    <section class="panel">
      <h2 class="panel__title">Preview</h2>
      <div class="profile-mini">
        ${u.picture_urls && u.picture_urls[0] ? `<img src="${escapeHtml(u.picture_urls[0])}" alt="">` : ""}
        <p><strong>${escapeHtml(u.name)}</strong> · ${u.age}</p>
        <p>${escapeHtml(u.bio || "")}</p>
      </div>
    </section>
    <section class="panel">
      <h2 class="panel__title">Act as user</h2>
      <label class="field">
        <span class="field__label">User</span>
        <select id="user-switch" class="field__input">
          ${options
            .map(
              (x) =>
                `<option value="${escapeHtml(x.username)}" ${x.username === state.session.username ? "selected" : ""}>${escapeHtml(x.name)} (${escapeHtml(x.username)})</option>`
            )
            .join("")}
        </select>
      </label>
    </section>
    <section class="panel">
      <h2 class="panel__title">Match preferences</h2>
      <form id="prefs-form" class="prefs-form">
        <fieldset class="prefs-gender">
          <legend>Show me</legend>
          <label><input type="checkbox" name="male" ${g.male ? "checked" : ""}> Men</label>
          <label><input type="checkbox" name="female" ${g.female ? "checked" : ""}> Women</label>
          <label><input type="checkbox" name="nonbinary" ${g.nonbinary ? "checked" : ""}> Non-binary</label>
        </fieldset>
        <label class="field">
          <span class="field__label">Min age</span>
          <input type="number" name="age_min" class="field__input" min="18" max="99" value="${prefs.age_min}">
        </label>
        <label class="field">
          <span class="field__label">Max age</span>
          <input type="number" name="age_max" class="field__input" min="18" max="99" value="${prefs.age_max}">
        </label>
        <label class="field">
          <span class="field__label">Distance (km)</span>
          <input type="number" name="distance_km" class="field__input" min="1" max="20000" value="${Math.round(prefs.distance_meters / 1000)}">
        </label>
        <button type="submit" class="btn btn--primary">Save preferences</button>
      </form>
    </section>`;
}

async function viewUser(username) {
  let data;
  try {
    data = await apiGet("action=user&username=" + encodeURIComponent(username));
  } catch (e) {
    return renderHeader("Profile", "") + `<p class="banner banner--error">${escapeHtml(String(e.message))}</p>`;
  }
  const u = data.user;
  const pics = u.picture_urls || [];
  const hero = pics[0] || "";
  const interests = (u.interests || []).map((x) => x.name || x.id).join(" · ");
  return `
    <a href="#/feed" class="back-link">← Back</a>
    ${renderHeader(u.name, u.location || "")}
    <article class="profile-card profile-card--static">
      <div class="profile-card__photo-wrap">
        ${hero ? `<img class="profile-card__photo" src="${escapeHtml(hero)}" alt="">` : ""}
      </div>
      <div class="profile-card__body">
        <h2 class="profile-card__name">${escapeHtml(u.name)}, ${u.age}</h2>
        <p class="profile-card__bio">${escapeHtml(u.bio || "")}</p>
        ${interests ? `<p class="profile-card__tags">${escapeHtml(interests)}</p>` : ""}
      </div>
    </article>`;
}

async function renderRoute() {
  const { route, arg } = parseHash();
  const app = document.getElementById("app");
  if (!app) return;

  let mainHtml = "";
  let navRoute = route;

  try {
    if (!state.session) await loadSession();
  } catch (e) {
    app.innerHTML = `<div class="shell"><p class="banner banner--error">${escapeHtml(String(e.message))}</p></div>`;
    return;
  }

  if (route === "feed") {
    mainHtml = await viewFeed();
  } else if (route === "likes") {
    mainHtml = await viewLikes();
  } else if (route === "matches") {
    mainHtml = await viewMatches();
  } else if (route === "chats") {
    mainHtml = await viewChats();
  } else if (route === "chat" && arg) {
    mainHtml = await viewChat(arg);
    navRoute = "chats";
  } else if (route === "profile") {
    mainHtml = await viewProfile();
  } else if (route === "user" && arg) {
    mainHtml = await viewUser(arg);
    navRoute = "feed";
  } else {
    location.hash = "#/feed";
    return;
  }

  app.innerHTML = `<div class="shell"><main class="main" id="main">${mainHtml}</main>${renderNav(navRoute)}</div>`;
  wireActions();
}

function wireActions() {
  document.querySelectorAll("[data-react]").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const user = btn.getAttribute("data-user");
      const type = btn.getAttribute("data-react");
      if (!user || !type) return;
      try {
        const res = await apiPost("action=feed_react", { username: user, type });
        if (res.match) {
          alert("It is a match!");
        }
        await renderRoute();
      } catch (e) {
        alert(e.message || String(e));
      }
    });
  });

  const sw = document.getElementById("user-switch");
  if (sw) {
    sw.addEventListener("change", async () => {
      const v = sw.value;
      try {
        await apiPost("action=session", { username: v });
        state.session = null;
        await loadSession();
        await renderRoute();
      } catch (e) {
        alert(e.message || String(e));
      }
    });
  }

  const pf = document.getElementById("prefs-form");
  if (pf) {
    pf.addEventListener("submit", async (ev) => {
      ev.preventDefault();
      const fd = new FormData(pf);
      const body = {
        preferences: {
          gender: {
            male: !!(pf.querySelector('input[name="male"]') && pf.querySelector('input[name="male"]').checked),
            female: !!(pf.querySelector('input[name="female"]') && pf.querySelector('input[name="female"]').checked),
            nonbinary: !!(pf.querySelector('input[name="nonbinary"]') && pf.querySelector('input[name="nonbinary"]').checked),
          },
          age_min: Number(fd.get("age_min")),
          age_max: Number(fd.get("age_max")),
          distance_meters: Math.round(Number(fd.get("distance_km")) * 1000),
        },
      };
      try {
        await apiPost("action=preferences", body);
        state.session = null;
        await loadSession();
        await renderRoute();
      } catch (e) {
        alert(e.message || String(e));
      }
    });
  }

  const cf = document.getElementById("chat-form");
  if (cf) {
    const withUser = cf.getAttribute("data-with");
    const input = document.getElementById("chat-input");
    cf.addEventListener("submit", async (ev) => {
      ev.preventDefault();
      const text = (input && input.value) || "";
      if (!text.trim() || !withUser) return;
      try {
        await apiPost("action=chat_send&with=" + encodeURIComponent(withUser), { message: text });
        if (input) input.value = "";
        await renderRoute();
        const log = document.getElementById("chat-log");
        if (log) log.scrollTop = log.scrollHeight;
      } catch (e) {
        alert(e.message || String(e));
      }
    });
    const log = document.getElementById("chat-log");
    if (log) log.scrollTop = log.scrollHeight;
  }
}

window.addEventListener("hashchange", () => renderRoute());
window.addEventListener("DOMContentLoaded", () => {
  if (!location.hash || location.hash === "#") location.hash = "#/feed";
  renderRoute();
});
