# SnapDB

Proyecto de control de versiones para bases de datos PostgreSQL. Permite realizar backups incrementales y gestionar el historial de cambios en la base de datos.

## Instalación

1. Clona el repositorio:

   ```bash
   git clone 
    ```

2. Navega al directorio del proyecto:

   ```bash
   cd SnapDB
   ```

3. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

Instalación en modo editable:

```bash
pip install -e .
```

## Uso

```bash
snapdb [OPTIONS] COMMAND [ARGS]...
```

**Opciones:**

- `--install-completion` — Instala el autocompletado para el shell actual.
- `--show-completion` — Muestra el autocompletado para el shell actual.
- `--help` — Muestra el mensaje de ayuda y sale.

**Comandos:**

- `use` — Selecciona la versión de PostgreSQL a utilizar.
- `version` — Muestra la versión actual.
- `fetch` — Muestra la lista de paquetes disponibles.
- `list` — Muestra la lista de paquetes instalados.
- `install` — Instala un paquete específico.
- `checkout` — Restaura el estado de la base de datos a un commit específico.
- `status` — Muestra el estado actual del staging.
- `logs` — Muestra el historial de commits.
- `init` — Inicializa un nuevo repositorio de control de versiones.
- `connections` — Muestra las conexiones disponibles.
- `connect` — Activa una conexión específica.
- `create-connection` — Crea una nueva conexión.
- `add` — Agrega un archivo de respaldo al staging.
- `commit` — Crea un nuevo commit con los archivos en staging.

## Screenshot

![alt text](image.png)
