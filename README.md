# BeerDin 🍺

Este es un bot de Discord desarrollado en Python que se encarga de recolectar métricas y datos de servidores de Discord, incluyendo el uso de emoticonos, mensajes, y estadísticas de voz.
Utiliza bases de datos PostgreSQL y MongoDB para almacenar y gestionar los datos, respetando la privacidad de los usuarios.

## Descripción
Este bot se conecta a un servidor de Discord y recolecta información sobre el servidor, como la cantidad de mensajes enviados, emoticonos más usados, tiempo en llamadas de voz y estadísticas de usuarios. Los datos son almacenados temporalmente en bases de datos PostgreSQL y MongoDB para un uso específico. Los usuarios pueden personalizar el comportamiento del bot mediante un archivo `.env` para gestionar las configuraciones como el prefijo de comandos, el idioma y las claves de acceso a la base de datos.

## Requisitos

- **Python 3.13.2**
- **uv**
- **Ruff**
- *(Opcional)* **Docker** y **Docker Compose**

## Instalación y ejecución con uv

1. **Instalar `uv`** (si no está ya instalado):
   ```bash
   pip install uv
   ```
   O consulta la [documentación oficial de uv](https://github.com/astral-sh/uv) para otras opciones de instalación.

2. **Clonar este repositorio**:
   ```bash
   git clone https://github.com/Afordin/beerdin
   cd beerdin
   ```

3. **Sincronizar dependencias**:
   ```bash
   uv sync
   ```
   - Esto creará o actualizará el entorno virtual `.venv` e instalará todas las dependencias (incluyendo Ruff).

4. **Ejecutar la aplicación** (usando el CLI de FastAPI, instalado dentro de `.venv`):
   ```bash
   uv run python app/main.py
   ```

## Usando Ruff con uv

Para ejecutar **Ruff** a través de uv, simplemente ejecuta:

```bash
uv run ruff check .
```

Esto analizará tu código y mostrará cualquier sugerencia de estilo o sintaxis.


## Ejecución con Docker

### Dockerfile

El **Dockerfile** incluido:
1. Utiliza una imagen base de Python slim.
2. Copia el binario de `uv`.
3. Copia el proyecto en `/app`.
4. Ejecuta `uv sync` para instalar las dependencias.
5. Utiliza `fastapi` para iniciar la aplicación dentro del contenedor.

### docker-compose.yml

También encontrarás un archivo **docker-compose.yml** para ejecutar el servicio. Úsalo de la siguiente manera:

```bash
docker-compose build
docker-compose up -d
```

Esto:
- **Construye** la imagen usando el Dockerfile.
- **Inicia** el bot.
