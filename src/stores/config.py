from pathlib import Path
import typer


class ConfigStore:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()

    def getConfigActive(self):
        self.cursor.execute("SELECT name, path FROM Config WHERE active = 1 LIMIT 1")
        result = self.cursor.fetchone()
        if result is None:
            print("\033[31mNo hay configuraciones activas.")
            raise typer.Exit()
        return {"name": result[0], "path": result[1]}

    def getConnections(self):
        self.cursor.execute(
            "SELECT name, active FROM Connections \
            WHERE id_config = (SELECT id FROM Config WHERE active = 1 LIMIT 1)"
        )
        return self.cursor.fetchall()

    def getActiveConnection(self):
        self.cursor.execute(
            "SELECT host, port, user, password, database FROM Connections "
            "WHERE id_config = (SELECT id FROM Config WHERE active = 1 LIMIT 1) "
            "AND active = 1 LIMIT 1"
        )
        result = self.cursor.fetchone()
        if result is None:
            print("\033[31mNo hay conexiones activas.\033[0m")
            raise typer.Exit()
        return {
            "host": result[0],
            "port": result[1],
            "user": result[2],
            "password": result[3],
            "database": result[4],
        }

    def configActive(self, path_current: Path):
        self.cursor.execute("UPDATE Config SET active = 0 WHERE active = 1")
        self.cursor.execute(
            "UPDATE Config SET active = 1 WHERE path = ?",
            (str(path_current),),
        )
        self.conn.commit()

    def connectionActive(self, name):
        self.cursor.execute(
            "UPDATE Connections SET active = 0 WHERE active = 1 AND id_config = (SELECT id FROM Config WHERE active = 1 LIMIT 1)"
        )
        self.cursor.execute(
            "UPDATE Connections SET active = 1 WHERE name = ? AND id_config = (SELECT id FROM Config WHERE active = 1 LIMIT 1)",
            (name,),
        )
        self.conn.commit()

    def createConnection(self, host, port, user, password, database, name):

        exist_name = self.cursor.execute(
            "SELECT name FROM Connections WHERE name = ? AND id_config = (SELECT id FROM Config WHERE active = 1 LIMIT 1)",
            (name,),
        ).fetchone()

        if exist_name:
            print(f"\033[31mYa existe una conexión con el nombre '{name}'.\033[0m")
            raise typer.Exit()

        self.cursor.execute(
            "UPDATE Connections SET active = 0 WHERE active = 1 AND id_config = (SELECT id FROM Config WHERE active = 1 LIMIT 1)"
        )
        self.cursor.execute(
            "INSERT INTO Connections (host, port, user, password, database, name, id_config, active) VALUES (?, ?, ?, ?, ?, ?, "
            "(SELECT id FROM Config WHERE active = 1 LIMIT 1), 1)",
            (host, port, user, password, database, name),
        )
        self.conn.commit()

    def createConfig(self, name):
        self.cursor.execute(
            "INSERT INTO Config (name, active, path) VALUES (?, ?, ?)",
            (name, 1, str(Path.cwd())),
        )
        self.conn.commit()
