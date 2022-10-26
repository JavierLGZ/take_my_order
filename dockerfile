FROM python:3.10-slim-bullseye

# Establece las variables de entorno
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV ACCEPT_EULA=Y

# Define el directorio de trabajo
WORKDIR /orderapi

# Copia el contexto de la aplicacion en el directorio de trabajo.
# Excluye los archivos señalados en .dockerfile
COPY . /orderapi

RUN pip install --upgrade pip \
    && pip install wheel \
    && pip install --no-cache-dir -r /orderapi/requirements.txt

# Ejecuta las migraciones
RUN python manage.py makemigrations \
    && python manage.py migrate

# Inicia el servidor de Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
