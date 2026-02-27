from helper.binaries import Packages
from helper.files import BackupFile
from helper.persistent import Store
from textwrap import dedent
import typer
from pathlib import Path


def banner():
    typer.echo(
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


app = typer.Typer(help="SnapDB: Control de versiones para bases de datos")
store = Store()
backup = BackupFile()
package = Packages()


store.configActive(Path.cwd())


@app.command()
def use(package: str):
    package_name = package
    store.updatePackage(package_name, True)
    typer.echo(f"Paquete '\033[32m{package_name}\033[0m' activado.")


@app.command()
def version():
    """Muestra la versión actual."""
    typer.echo("Version 1.0.0")


@app.command()
def fetch():
    """Muestra la lista de paquetes disponibles."""
    packages = package.fetch("postgres")
    for pkg in packages:
        typer.echo(f"- {pkg['name']} \033[33m[{pkg['title']}]\033[0m")


@app.command()
def list():
    """Muestra la lista de paquetes instalados."""
    packages = store.getPackages()
    for pkg in packages:
        typer.echo(
            f"- {pkg['name']} \033[32m{'(activo)' if pkg['active'] else ''}\033[0m"
        )


@app.command()
def install(package_name: str):
    """Instala un paquete específico."""
    package.install(package_name)


@app.command()
def checkout(commit: str):
    """Restaura el estado de la base de datos a un commit específico."""
    typer.echo(f"Checkout al commit \033[33m'{commit}'\033[0m")

    commit_data = store.getCommit(commit)

    backup.execute(commit_data["file_name"])


@app.command()
def status():
    """Muestra el estado actual del staging."""
    files = store.getStaging()
    for file in files:
        typer.echo(f"  - {file[0]}")


@app.command()
def logs():
    """Muestra el historial de commits."""
    logs = store.getLogs()
    for log in logs:
        typer.echo(
            dedent(
                f"""
                \033[33mCommit:\033[0m '{log['message']}'
                \033[33mHash:\033[0m {log['hash']}
                \033[33mFecha:\033[0m {log['timestamp']}
                """
            )
        )


@app.command()
def init(name: str):
    """Inicializa un nuevo repositorio de control de versiones."""
    store.createConfig(name)
    typer.echo(f"Configuración '{name}' creada y activada.")


@app.command()
def connections():
    """Muestra las conexiones disponibles."""
    connections = store.getConnections()
    for conn in connections:
        typer.echo(f"- {conn[0]} \033[32m{'(activo)' if conn[1] else ''}\033[0m")


@app.command()
def connect(name: str):
    """Activa una conexión específica."""
    store.connectionActive(name)
    typer.echo(f"Conexión '\033[32m{name}\033[0m' activada.")


@app.command("create-connection")
def create_connection(
    name: str,
    host: str = typer.Option(..., "--host", "-H", help="Host de la base de datos"),
    port: int = typer.Option(..., "--port", "-P", help="Puerto de la base de datos"),
    user: str = typer.Option(..., "--user", "-U", help="Usuario de la base de datos"),
    password: str | None = typer.Option(
        None,
        "--password",
        "-p",
        help="Contraseña de la base de datos",
    ),
    database: str = typer.Option(
        ..., "--database", "-d", help="Nombre de la base de datos"
    ),
):
    """Crea una nueva conexión."""
    store.createConnection(host, port, user, password, database, name)
    typer.echo(f"Conexión '\033[32m{name}\033[0m' creada.")


@app.command()
def add(file_path: str):
    """Agrega un archivo de respaldo al staging."""
    pathFile = backup.backup(file_path)
    store.addStaging(pathFile)
    typer.echo(f"Archivo '{file_path}' agregado al staging.")


@app.command()
def commit(message: str):
    """Crea un nuevo commit con los archivos en staging."""
    hash_value = store.commit(message)

    if hash_value:
        typer.echo(
            f"\033[33mCommit:\033[0m'{message}'\033[33m hash:\033[0m {hash_value}"
        )


@app.callback()
def main(ctx: typer.Context):
    banner()
    isInit = ctx.invoked_subcommand == "init"
    isCreateConnection = ctx.invoked_subcommand == "create-connection"

    if isInit or isCreateConnection:
        return

    connect = store.getActiveConnection()

    backup.setCredentials(
        host=connect["host"],
        port=connect["port"],
        user=connect["user"],
        password=connect["password"],
        database=connect["database"],
    )


if __name__ == "__main__":
    app()
