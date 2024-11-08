import os


class Config:
    DATABASE_FILE = os.getenv("DATABASE_FILE", "database.json")
    SECRET_KEY = "c7ce9437b54c40d7ab2e92cad2e0827d"
