# participacion_consulta
Sistema para registrar consultas provenientes del gestor de consulta


## Instalación
  
```
mkvirtualenv participacion_consulta -p /usr/bin/python3
pip install -r requirements.txt
```

## Crear migraciones

```
python manage.py makemigrations users
python manage.py makemigrations participacion

python manage.py migrate
```

## Configurar en el setting

Se debe modificar en el `settings.py` la constante `API_BASE_URL` con la url y puerto del gestor de consulta y se deben insertar los tokens correspondientes de consultas en `CONSULTA_SECRET_TOKEN`

## Correr aplicación

  `python manage.py runserver`