import tarfile
import zipfile
from helper.compress import ExtractFileZip, ExtractFileTar
import requests
import sys
import os
from pathlib import Path
import typer


class DownloadFile:
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent.parent

    def download(self, url, output_path):
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            total = int(response.headers.get("content-length", 0))
            downloaded = 0
            with open(output_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    downloaded += len(chunk)

                    percent = downloaded * 100 / total if total > 0 else 0
                    sys.stdout.write(
                        f"\rDescargando... \033[32m{percent:.2f}%\033[0m  ({downloaded}/{total} bytes)"
                    )
                    sys.stdout.flush()

            return output_path

        except requests.RequestException as e:
            typer.echo(f"\033[31mError al descargar el archivo: {e}\033[0m")
            raise typer.Exit()

    def extract(self, path, extract_to, extension):
        try:
            extractors = {
                "zip": ExtractFileZip(),
                "tar": ExtractFileTar(),
                "tar.gz": ExtractFileTar(),
            }

            extractor = extractors.get(extension)

            if extractor is not None:
                return extractor.extract(path, extract_to)

            typer.echo(f"\033[31mFormato de archivo no soportado: {extension}\033[0m")
            raise typer.Exit()

        except zipfile.BadZipFile as e:
            typer.echo(f"\033[31mError al extraer el archivo ZIP: {e}\033[0m")
            raise typer.Exit()
        except tarfile.TarError as e:
            typer.echo(f"\033[31mError al extraer el archivo TAR: {e}\033[0m")
            raise typer.Exit()

    def downloadAndExtract(self, url, extract_to, extension):
        zip_path = self.base_dir / "binaries/" 

        if not os.path.exists(zip_path):
            os.makedirs(zip_path)

        zip_path = zip_path / f"temp.{extension}"
        
        path = self.download(url, zip_path)
        self.extract(path, extract_to, extension)
        os.remove(path)
