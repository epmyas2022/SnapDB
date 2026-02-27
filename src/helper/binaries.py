import re
from pathlib import Path
import requests
import platform
from helper.download import DownloadFile
from helper.persistent import Store
import typer


class Packages:
    def __init__(self):
        self.repository_url = "https://raw.githubusercontent.com/epmyas2022/SnapDB/refs/heads/main/packages.json"
        self.base_dir = Path(__file__).resolve().parent.parent
        self.store = Store()

    def install(self, package):
        pattern = r"^@(?P<platform>[\w-]+)/(?P<driver>[\w-]+)-(?P<version>[\d\.]+)$"

        match = re.match(pattern, package)

        if not match:
            print(
                f"\033[31mEl formato'{package}' es inválido. Use '@platform/driver-version'.\033[0m"
            )
            raise typer.Exit()

        driver = match.group("driver")
        data = self.fetch(driver)

        find = list(filter(lambda x: x["name"] == package, data))

        if find is None or len(find) == 0:
            print(
                f"\033[31mPaquete '{package}' no encontrado para el driver '{driver}'.\033[0m"
            )
            raise typer.Exit()

        download = DownloadFile()

        download.downloadAndExtract(
            find[0]["url"],
            self.base_dir / "binaries" / package,
            find[0]["type"],
        )

        self.store.addPackage(package, find[0]["bin"])

    def fetch(self, driver):
        result = requests.get(self.repository_url)

        types = {"windows": "windows", "darwin": "macos", "linux": "linux"}

        filter_platform = types.get(platform.system().lower(), "windows")

        if result.status_code != 200:
            print("Error al obtener la lista de paquetes.")
            raise typer.Exit()

        data = result.json()[driver]
        data = list(filter(lambda x: x["platform"].startswith(filter_platform), data))
        return map(
            lambda x: {
                "name": f"@{x['platform']}/{driver}-{x['version']}",
                "title": x["name"],
                "platform": x["platform"],
                "url": x["url"],
                "bin": x.get("bin", ""),
                "type": x.get("type", "zip"),
            },
            data,
        )
