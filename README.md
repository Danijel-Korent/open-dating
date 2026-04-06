# Flask Dating App

A small app for prototyping

## Usage

- If desired, create a virtual environment and activate it. (Highly recommended)
- Install the requirements with `pip install -r requirements.txt`.
- Select a database file by running `flask db select-database <path>` or edit `DATABASE_FILE` in the `.env`
- Run `python run.py` in the root directory
- In folder `/assets`
  - Run `npm install`
  - Run `npm run dev`

## Code structure

Overview of the main folders (see [ARCHITECTURE.md](ARCHITECTURE.md) for detail):

```
.
├── app/                        Flask application package
│   ├── __init__.py             App factory, blueprints, Socket.IO
│   ├── db.py                   JSON-backed database layer
│   ├── config.py               Configuration
│   ├── routes.py               Session, context processors, shared routes
│   ├── algo.py                 Feed recommendation scoring
│   ├── util.py                 Utilities
│   ├── api/                    /api blueprint
│   ├── dating/                 Main dating UI routes and templates
│   ├── messages/               Chat routes, templates, Socket.IO handlers
│   ├── communities/            Communities routes and templates
│   ├── static/                 Built JS/CSS (dist/) and images
│   └── templates/              Base templates, includes, navigation
├── assets/                     Frontend source (Webpack, Tailwind, TypeScript)
│   ├── package.json            NPM scripts and dependencies
│   ├── webpack.config.js
│   └── ts/                     TypeScript entry and Alpine components
├── run.py                      Dev server entry (Socket.IO + Flask)
├── requirements.txt            Python dependencies
└── ARCHITECTURE.md             Architecture and design notes
```
