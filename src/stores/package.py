class PackageStore:
    def __init__(self, cursor, conn):
        self.cursor = cursor
        self.conn = conn
    
    def updatePackage(self, package_name, active):
        self.cursor.execute(
            "UPDATE Packages SET active = 0 WHERE active = 1"
        )
        self.cursor.execute(
            "UPDATE Packages SET active = ? WHERE package_name = ?",
            (1 if active else 0, package_name),
        )
        self.conn.commit()

    def addPackage(self, package_name):

        existing_package = self.cursor.execute(
            "SELECT package_name FROM Packages WHERE package_name = ?",
            (package_name,),
        ).fetchone()

        if existing_package: return
        
        self.cursor.execute(
            "INSERT INTO Packages (package_name) VALUES (?)",
            (package_name,),
        )
        self.conn.commit()

    def getActivePackage(self):
        self.cursor.execute("SELECT package_name FROM Packages WHERE active = 1 LIMIT 1")
        result = self.cursor.fetchone()
        if result is None:
            print("\033[31mNo hay paquetes activos. Use 'snapdb --use @platform/driver-version' para activar uno.\033[0m")
            exit(1)
        return result[0]
    
    def getPackages(self):
        self.cursor.execute("SELECT package_name, active FROM Packages")
        result = self.cursor.fetchall()

        return map(
            lambda x: {"name": x[0], "active": bool(x[1])},
            result,
        )
