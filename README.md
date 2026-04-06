# Dating App Prototype

A small app for prototyping

## Usage

Serve it from a web server with PHP support

## Technical

Vanilla PHP backend + vanilla JS SPA frontend

## Code structure

Overview of the main folders:

```
.
├── backend/                    PHP API and image serving (no URL rewriting)
│   ├── api.php                 JSON API; dispatch via ?action=…
│   ├── image.php               Serves files under data/images/ safely
│   └── lib/
│       ├── store.php           Load/save database.json with flock
│       ├── service.php         Feed, likes, matches, chats, react
│       └── pictures.php        Picture URL helpers and path validation
├── data/
│   ├── database.json           Single source of truth (users, likes, matches, chats, …)
│   └── images/                 Profile and shared images (e.g. avatar.png, <username>/…)
├── js/
│   ├── api.js                  fetch helpers for backend/api.php
│   └── app.js                  Hash-router SPA (views, navigation)
├── index.html                  SPA shell
├── styles.css                  Vanilla CSS
└── LICENSE
```
