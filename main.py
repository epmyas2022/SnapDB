import argparse
import sys
from helper.binaries import Packages
from helper.files import BackupFile
from helper.persistent import Store
from textwrap import dedent


def banner():
    print(
        """
\033[32m
███████╗███╗   ██╗ █████╗ ██████╗     ██████╗ ██████╗ 
██╔════╝████╗  ██║██╔══██╗██╔══██╗    ██╔══██╗██╔══██╗
███████╗██╔██╗ ██║███████║██████╔╝    ██║  ██║██████╔╝
╚════██║██║╚██╗██║██╔══██║██╔═══╝     ██║  ██║██╔══██╗
███████║██║ ╚████║██║  ██║██║         ██████╔╝██████╔╝
╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝         ╚═════╝ ╚═════╝ 

@github.com/epmyas2022 | 2026-02-24

\033[0m
"""
    )


def parser():
    parser = argparse.ArgumentParser(
        description="Control de versiones para bases de datos"
    )
    parser.add_argument(
        "--version",
        help="Muestra la versión de la aplicación",
        action="store_true",
    )
    parser.add_argument(
        "--fetch", help="Obtiene la lista de paquetes disponibles", action="store_true"
    )
    parser.add_argument("--install", type=str, help="Instala un paquete específico")
    parser.add_argument(
        "--logs", help="Muestra el historial de commits", action="store_true"
    )
    parser.add_argument(
        "--status", help="Muestra los backups en staging", action="store_true"
    )
    parser.add_argument("--checkout", type=str, help="Ir a un commit específico")
    parser.add_argument(
        "--init", type=str, help="Inicializa el repositorio de control de versiones"
    )
    parser.add_argument("--add", type=str, help="Agrega un nuevo cambio al repositorio")
    parser.add_argument(
        "--commit", type=str, help="Realiza un commit de los cambios agregados"
    )

    if sys.argv[1:] == []:
        parser.print_help()
        return

    args = parser.parse_args()

    return args


def main():
    banner()
    args = parser()
    if args is None:
        return

    store = Store()
    backup = BackupFile()
    package = Packages()

    backup.setCredentials(
        host="localhost",
        port=5432,
        user="postgres",
        password="postgres",
        database="postgres",
    )

    if args.version:
        print("Version 1.0.0")

    if args.fetch:
        packages = package.fetch("postgres")
        for pkg in packages:
            print(f"- {pkg['name']} \033[33m[{pkg['title']}]\033[0m")

    if args.install:
        package.install(args.install)

    if args.checkout:
        print(f"Checkout al commit \033[33m'{args.checkout}'\033[0m")

        commit = store.getCommit(args.checkout)

        backup.execute(commit["file_name"])

    if args.status:
        files = store.getStaging()
        for file in files:
            print(f"  - {file[0]}")

    if args.logs:
        logs = store.getLogs()
        for log in logs:
            print(
                dedent(
                    f"""
                \033[33mCommit:\033[0m '{log['message']}'
                \033[33mHash:\033[0m {log['hash']}
                \033[33mFecha:\033[0m {log['timestamp']}
                """
                )
            )
    if args.init:
        print("Repositorio de control de versiones inicializado.")

    if args.add:
        pathFile = backup.backup(args.add)
        store.addStaging(pathFile)
        print(f"Archivo '{args.add}' agregado al staging.")

    if args.commit:
        hash_value = store.commit(args.commit)

        if hash_value:
            print(
                f"\033[33mCommit:\033[0m'{args.commit}'\033[33m hash:\033[0m {hash_value}"
            )


if __name__ == "__main__":
    main()
