# Artículos-Categoría-API

# Instalación sin docker
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000


## Requisitos

- Python 3.10+
- Docker y Docker Compose

## Instalación

1. Crea un entorno virtual:
   ```bash
   python3 -m venv .venv
   ```
2. Activa el entorno:

   ```bash
   # Linux / macOS
   source .venv/bin/activate

   # Windows (cmd)
   .venv\Scripts\activate.bat

   # Windows (PowerShell)
   .venv\Scripts\Activate.ps1
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Base de Datos

Levanta MariaDB con Docker Compose:

```bash
docker-compose up -d
```

## Ejecución

Arranca la API:

```bash

uvicorn app.main:app --reload --port 8000
```

## Pruebas

Usa el archivo `test.http` con el VSCode REST Client para probar los endpoints.
