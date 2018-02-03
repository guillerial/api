# API 

Instrucciones de instalación de un venv:
```bash
python3 -m venv .venv
```

Esto creará el directorio .venv

Utilizar la API:
```bash
source .venv/bin/activate
./api/api/manage.py migrate
./api/api/manage.py runserver 0.0.0.0:8000
```
