import hashlib
import typer

class ControlStore:
    def getStaging(self):
        self.cursor.execute("SELECT file_name FROM Staging WHERE id_config = (SELECT id FROM Config WHERE active = 1 LIMIT 1)")
        return self.cursor.fetchall()

    def getLogs(self):
        self.cursor.execute(
            "SELECT hash, message, file_name, timestamp FROM Commits " 
            "WHERE id_config = (SELECT id FROM Config WHERE active = 1 LIMIT 1) ORDER BY timestamp DESC"
        )
        result = self.cursor.fetchall()

        return map(
            lambda x: {
                "hash": x[0],
                "message": x[1],
                "file_name": x[2],
                "timestamp": x[3],
            },
            result,
        )

    def getCommit(self, hash_value):
        self.cursor.execute(
            "SELECT hash, message, file_name FROM Commits WHERE hash = ? LIMIT 1",
            (hash_value,),
        )
        result = self.cursor.fetchone()
        if result is None:
            print(f"\n\033[31mCommit con hash '{hash_value}' no encontrado.\033[0m")
            raise typer.Exit()
        return {
            "hash": result[0],
            "message": result[1],
            "file_name": result[2],
        }

    def addStaging(self, file_name):
        self.cursor.execute(
            "INSERT INTO Staging (file_name, id_config) VALUES"
            "(?, (SELECT id FROM Config WHERE active = 1 LIMIT 1))",
            (file_name,),
        )
        self.conn.commit()

    def commit(self, message):
        self.cursor.execute("SELECT file_name FROM Staging")
        files = self.cursor.fetchall()
        if not files:
            print("\033[31mNo hay archivos para commitear.\033[0m")
            return

        for file in files:
            file_name = file[0]
            hash_value = self.generate_hash(file_name)
            self.cursor.execute(
                "INSERT INTO Commits (hash, message, file_name, id_config) VALUES"
                    "(?, ?, ?, (SELECT id FROM Config WHERE active = 1 LIMIT 1))",
                (hash_value, message, file_name),
            )
        self.cursor.execute("DELETE FROM Staging")
        self.conn.commit()
        return hash_value

    def generate_hash(self, file_name):
        contentFile = open(file_name, "rb").read()
        hash_object = hashlib.sha256(contentFile)
        return hash_object.hexdigest()
