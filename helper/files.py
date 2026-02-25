import subprocess
import os
from pathlib import Path
from datetime import datetime


class BackupFile:
    def __init__(
        self,
        path="./backups",
        driver="postgres",
    ):
        self.path = path
        self.driver = driver
        self.platform = os.name
        self.base_dir = Path(__file__).resolve().parent.parent
        self.env = os.environ.copy()

    def __binary_path(self, command):
        binary_path = (
            self.base_dir / "binaries" / "windows" / "pgsql" / "bin" / f"{command}.exe"
        )
        return binary_path.resolve()

    def setCredentials(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.env["PGPASSWORD"] = password
        self.database = database

    def execute(self, pathFile):
        self.dropAll()
        binary_path = self.__binary_path("pg_restore")
        
        if not os.path.exists(binary_path):
            print(f"\033[31mpg_restore no encontrado en {binary_path}\033[0m")
            exit(1)

        result = subprocess.run(
            [
                binary_path,
                "-h",
                self.host,
                "-p",
                str(self.port),
                "-U",
                self.user,
                "-d",
                self.database,
                pathFile,
            ],
            env=self.env,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(f"\033[31mError al ejecutar: {result.stderr}\033[0m")
            exit(1)

    def dropAll(self):
        binary_path = self.__binary_path("psql")
        result = subprocess.run(
            [
                binary_path,
                "-h",
                self.host,
                "-p",
                str(self.port),
                "-U",
                self.user,
                "-d",
                self.database,
                "-c",
                "DROP SCHEMA public CASCADE; CREATE SCHEMA public;",
            ],
            env=self.env,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(f"\033[31mError al ejecutar: {result.stderr}\033[0m")
            exit(1)

    def backup(
        self,
        name="backup",
        user="postgres",
        dbname="postgres",
    ):
        
        binary_path = self.__binary_path("pg_dump")

        if not os.path.exists(binary_path):
            print(f"\033[31mpg_dump no encontrado en {binary_path}\033[0m")
            exit(1)

        output_path = (
            self.base_dir
            / self.path
            / f"{name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.dump"
        )

        result = subprocess.run(
            [
                binary_path,
                "-h",
                self.host,
                "-p",
                str(self.port),
                "-U",
                user,
                "-d",
                dbname,
                "--no-owner",
                "--no-privileges",
                "--format=custom",
                "-b",
                "-v",
                "-f",
                str(output_path),
            ],
            env=self.env,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(f"\033[31mError al ejecutar pg_dump: {result.stderr}\033[0m")
            exit(1)

        return str(output_path)
