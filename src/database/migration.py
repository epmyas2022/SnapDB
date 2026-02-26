from sqlite3 import Cursor


def migrate(cursor: Cursor):

    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS Config (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                path TEXT,
                active BOOLEAN NOT NULL DEFAULT 0,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
    )

    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS Connections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_config INTEGER,
                host TEXT NOT NULL,
                port INTEGER NOT NULL,
                user TEXT NOT NULL,
                password TEXT NOT NULL,
                database TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                name TEXT NOT NULL,
                active BOOLEAN NOT NULL DEFAULT 0,

                FOREIGN KEY (id_config) REFERENCES Config(id) ON DELETE CASCADE
            )
            """
    )
    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS Staging (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_name TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                id_config INTEGER,

                FOREIGN KEY (id_config) REFERENCES Config(id) ON DELETE CASCADE
            )
            """
    )
    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS Commits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hash TEXT NOT NULL,
                message TEXT NOT NULL,
                file_name TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,

                id_config INTEGER,

                FOREIGN KEY (id_config) REFERENCES Config(id) ON DELETE CASCADE
            )
            """
    )

    cursor.execute(
        """ 
            CREATE TABLE IF NOT EXISTS Packages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                package_name TEXT NOT NULL,
                active BOOLEAN NOT NULL DEFAULT 0,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
    )
