# Take my order



## Instrucciones

En la carpeta raiz se encuentran los archivos Dockerfile y docker-compose.yml. Estos contienen la informacion necesaria para un arranque por medio de esta tecnologia. Para iniciar abre una terminal en la ubicacion del repositorio y con el comando: `docker-compose up` iniciaremos la contruccion de la imagen, el montaje y ejecucion del contenedor con los parametros necesarios para su funcionamiento.

> NOTA: docker compose ya viene preinstalado con docker desktop para windows, en linux debe ser instalado por aparte

una ves ejecutado podemos dirigirnos a la direccion [localhost:8000/order](http://localhost:8000/order/) para pode interactuar con la API
en la direccion [localhost:8000/swagger](http://localhost:8000/swagger/) podemos encontrar informacion mas detallada de la API sobre los metodos disponibles y los parametros necesarios la respuesta satisfactoria de la API
