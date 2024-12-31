# Flask Dating App

## Usage

- If desired, create a virtual environment and activate it. (Highly recommended)
- Install the requirements with `pip install -r requirements.txt`.
- Select a database file by running `flask db select-database <path>` or edit `DATABASE_FILE` in the `.env`
- Run `python main.py` in the root directory
- Run `npm run dev` in `/assets`

## Code structure

The below is a tree of the most important files and folders in the project:

```
.
├── open-dating/                Contains the project code
│   ├── __init__.py             Entry point
│   ├── db.py                   Database logic
│   ├── config.py               Flask application configuration
│   ├── routes.py               Defines application routes
│   ├── util.py                 Contains utility functions
│   ├── static/                 Static assets
│   └── templates/              HTML templates, macros, etc 
├── requirements.txt            Project dependencies
├── tailwind.config.js          Tailwind configuration
└── package.json                NPM packages and scripts
```
