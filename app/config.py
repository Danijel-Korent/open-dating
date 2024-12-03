import os


class Config:
    DATABASE_FILE = os.getenv("DATABASE_FILE", "database.json")
    WEBPACK_MANIFEST_PATH = "./static/dist/manifest.json"
