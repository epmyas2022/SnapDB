import re
from pathlib import Path
import requests

from helper.files import DownloadFile
from helper.persistent import Store

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
            exit(1)

        driver = match.group("driver")
        data = self.fetch(driver)

        find = list(filter(lambda x: x["name"] == package, data))[0]

        if find is None:
            print(
                f"\033[31mPaquete '{package}' no encontrado para el driver '{driver}'.\033[0m"
            )
            exit(1)

        download = DownloadFile()

        download.downloadAndExtract(find["url"], self.base_dir / "binaries" / package)

        self.store.addPackage(package)

    def fetch(self, driver):
        result = requests.get(self.repository_url)

        if result.status_code != 200:
            print("Error al obtener la lista de paquetes.")
            exit(1)

        data = result.json()[driver]
        return map(
            lambda x: {
                "name": f"@{x['platform']}/{driver}-{x['version']}",
                "title": x["name"],
                "platform": x["platform"],
                "url": x["url"],
            },
            data,
        )
