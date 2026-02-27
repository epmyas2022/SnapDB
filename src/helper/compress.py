from abc import ABC, abstractmethod
import zipfile
import tarfile
import sys
import typer


class ExtractFile(ABC):
    def __init__(self):
        pass
    @abstractmethod
    def extract(self, path, extract_to):
        pass
        

class ExtractFileZip(ExtractFile):
    def extract(self, path, extract_to):
        try:
            sys.stdout.write(f"\n\033[33mExtrayendo...\033[0m")
            with zipfile.ZipFile(path, "r") as zip_ref:
                total_files = len(zip_ref.infolist())
                for i, member in enumerate(zip_ref.infolist(), start=1):
                    zip_ref.extract(member, extract_to)
                    sys.stdout.write(
                        f"\033[33m\rExtrayendo.... ({i}/{total_files})\033[0m"
                    )
                    sys.stdout.flush()
        except zipfile.BadZipFile as e:
            typer.echo(f"\033[31mError al extraer el archivo ZIP: {e}\033[0m")
            raise typer.Exit()

class ExtractFileTar(ExtractFile):
    def extract(self, path, extract_to):
        try:
            sys.stdout.write(f"\n\033[33mExtrayendo...\033[0m")
            with tarfile.open(path, "r:*") as tar_ref:
                members = tar_ref.getmembers()
                total_files = len(members)
                for i, member in enumerate(members, start=1):
                    tar_ref.extract(member, extract_to)
                    sys.stdout.write(
                        f"\033[33m\rExtrayendo.... ({i}/{total_files})\033[0m"
                    )
                    sys.stdout.flush()

        except tarfile.TarError as e:
            typer.echo(f"\033[31mError al extraer el archivo TAR: {e}\033[0m")
            raise typer.Exit()
