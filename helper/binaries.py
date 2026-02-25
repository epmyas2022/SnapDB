from zipfile import Path


class Packages:
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent.parent

    def fetch(self, package_name):

        return "Lista de binarios de postgres"
