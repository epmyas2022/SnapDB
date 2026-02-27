import sqlite3
from database.migration import migrate
from stores.config import ConfigStore
from stores.control import ControlStore
from stores.package import PackageStore
from pathlib import Path
import sys


class Store(PackageStore, ControlStore, ConfigStore):
    def __init__(self, db_name="tree.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.get_base_dir() / self.db_name)
        self.cursor = self.conn.cursor()
        self.create_table()
    def get_base_dir(self):
        if getattr(sys, "frozen", False):
            # Ejecutable
            return Path(sys.executable).parent
        else:
            # Desarrollo
            return Path(__file__).resolve().parent.parent
    def create_table(self):
        migrate(self.cursor)
        self.conn.commit()
