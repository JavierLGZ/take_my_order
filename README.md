# Take my order

Take my order es una API que empareja clientes con repartidores.
El objetivo es que dadas las coordenadas de recogida y de entrega la api te empareje con el repartidor más cercano disponible.

## Instrucciones

En la carpeta raíz se encuentran los archivos Dockerfile y docker-compose.yml. Estos contienen la información necesaria para un arranque por medio de esta tecnología. Para iniciar abre una terminal en la ubicación del repositorio y con el comando: `docker-compose up` iniciaremos la construcción de la imagen, el montaje y ejecución del contenedor con los parámetros necesarios para su funcionamiento.

> NOTA: Docker compose ya está preinstalado con Docker desktop para Windows, en Linux debe ser instalado por aparte

Una vez ejecutado podemos dirigirnos a la dirección [localhost:8000/order](http://localhost:8000/order/) para poder interactuar con la API.
En la dirección [localhost:8000/swagger](http://localhost:8000/swagger/) podemos encontrar información más detallada de la API sobre los métodos disponibles y los parámetros necesarios para la respuesta satisfactoria de la API.
