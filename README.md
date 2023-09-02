# proyecto_final_topgunlab_CFL

Blog

Este proyecto es una aplicación desarrollada con el lenguaje de programación Python mediante el framework Django.

Se crea una API rest para la visualización y manipulacipón de la información que se encuentra en la base de datos la cual se trabaja con PostgreSQL.

Inicialmente se crea el entorno virtual donde se alojaran todos aquellos paquetes necesarios para el funcionamiento del proyecto. Para ello se trabaja con venv para el entorno virtual y la instalación de los paquetes se trabaja con Pip.

Los paquetes instaldos son realcionados en el archivo requirements.txt

En el archivo ".gitignore" se agregan los archivos y carpetas que no se suben al repositorio de GitHub.

Se crea el repositorio el GitHub llamado proyecto_final_topgunlab_CFL en el ambiente de desarrollo y se clona para dar inicio.

Habilitado el entorno virtual se procede a la instalación de los paquetes "Django" y "psycopg2-binary". Con Django se crea el proyecto "blog" y se actualiza el archivo "settings.py" para configurar la base de datos gracias al paquete psycopg2-binary..

y el paquete "psycopg2-binary" que se encarga de la comunicación con la base de datos

Para tener un control de las normas sugeridas en la Guía de Estilos para el Código de Python, se trabaja con el paquete flake8 y se crea un archivo con el mismo nombre donde se agrega aquellos tipos de archivo que no se requiere corroborar. La ejecución se realiza junto con los test para verificar y corregir las líneas que no cumplen con la guía y tener un código ordenado y estandarizado.

Respecto a las pruebas Unittest, cada aplicación cuenta con su carpeta y los archivos necesarios para realizar los tests. La metodología es que primero se realizan los tests y posteriormente se realiza el código. En ocaciones, y por falta de tiempo, primero se realizaba el código y después los tests o no se realizaban los tests y se procedia directamente a códificar.

En el archivo "urls.py" se agregan las rutas para la visualización en la web del admin de Django y las rutas de API del proyecto.

El proyecto gira entorno a la aplicación "core", la cual se agrega al archivo settings.py, donde se encuentran:

- El archivo models.py para la creación de la base de datos y las tablas para el administrador, usuarios, post y comentarios del blog.
- El archivo wait_for_db.py ubicado en la ruta core/management/commands/, con lo que se controla que la base de datos este disponible para la ejecución de los test y el cirre de esta una vez se han finalizado las pruebas.
- El archivo admin.py el cual se configura para la visualización de la web de Django admin.
- La carpeta migrations con los cambios realizados en el archivo models.py.
- Una carpeta "test" que contiene los archivos test_admin.py, test_commands.py y test.models.py los cuales se encargan de probar el código de los archivos wait_for_db.py, admin.py y models.py.

Las siguientes aplicaciones a instalar requieren de los paquetes djangorestframework y drf-spectacular.

La segunda aplicación a instalar es "user" la cual se encargará de la administración de los usuarios desde la API res. Se agrega la app en el archivo "settings.py". En esta se encuentra:

- La carpeta tests donde se agrega el archivo test.py para probar el funcionamiento del código del archivo serializer.py.
- El archivo "serializer.py" se codifica para la visualización y administración de la API basada en las clases y métodos del archivo "models.py" para los usuarios (crud y token).
- Para la visualización en el navegador web se agregan las rutas en el archivo "urls". Una vez agregadas se incluyen en el archivo urls.py del proyecto blog.
Por último tenemos el archivo views.py el cual se encarga de como se visualiza la API desde el navegador.

Posteriormente se realiza la instalación de la aplicación "post" que se encarga de la administración de los posts de los usuarios. En esta se instalan el paquete django-filter, para agregar un search para el título del post y fecha de creación, y el paquete request, el cual se encarga de realizar la petición a la API Rest "https://restcountries.com/v3.1/all". Dentro de la app se encuentra:

- Carpeta tests con el archivo test para realizar las pruebas de funcionamiento del serializer.py.
- Archivo serializers encargado del crud de los posts de los usuarios registrados.
- El archivo urls que agrega la ruta gracias a rest_framework.routers donde se puede importar las vistas y mediante views.PostViewSet registrar con routers la url de la app para ser agregadas en la API REST.
- Y el último, el archivo views.py para la visualización de la API en el navegador.

La última app a ser instalada es "comments" que se encarga de la administación de los comentarios que se realizan a cada uno de los posts. Dentro se encuentra:

- Carpeta tests con el archivo test para realizar las pruebas de funcionamiento del serializer.py (No se diligenció el archivo).
- Archivo serializers encargado del crud de los comentarios de los usuarios registrados.
- El archivo urls que agrega la ruta gracias a rest_framework.routers donde se puede importar las vistas y mediante views.PostViewSet registrar con routers la url de la app para ser agregadas en la API REST.
- Y el último, el archivo views.py para la visualización de la API en el navegador.

Funcionamiento de la API REST blog

1. Se ingresa a la ruta http://127.0.0.1:8000/api/docs/

2. User
2.1 Por primera vez crear un usuario en user-POST y agregar los datos, si ya existe un usuario pasar directamente al paso 2.1.
2.2. En user-POST /api/user/token/ botón "Try it out" se crea el token de autenticacón.
2.3. En la parte superior dar click en botón Authorize y en el modal emergente, la última opción tokenAuth (apiKey), se escribre "Token #######" (#: El valor entregado de token)
2.4. Ir a user-GET /api/user/me/ y verificar si devuelve valores del usuario actual registrado.
2.5. Si la autenticación es correcta se pueden actualizar todos los datos en user-PUT y si solo se desea alguno de los campos se realiza en user-PATCH

3. Post
3.1. Por primera vez crear un post en postposts-POST y agregar los datos.
3.2. Si ya existen post dar click en postposts-GET.
3.2.1 Se pueden para listar todos los posts existentes.
3.2.2 Se puede utiliazar el search para buscar por título o por fecha de creación del post.
3.3. Ir a postposts-GET /api/postposts/{id}/ y ver un post específico con toda la información de acuerdo al id del post requerido.
3.4. Para actualizar todos los datos en postposts-PUT y si solo se desea alguno de los campos se realiza en postposts-PATCH

4. Commets
4.1 Por primera vez crear un comment en commentscommnents-POST y agregar el dato del id del post a comentar y el comentario.
4.2 Si ya existen comments dar click en commentscommnents-GET para listar todos los comments existentes.
4.3. Ir a commentscommnents-GET /api/commentscommnents/{id}/ y ver un comentario específico con toda la información de acuerdo al id del comment requerido.
4.4. Para actualizar todos los datos en commentscommnents-PUT y si solo se desea alguno de los campos se realiza en postposts-PATCH

5. Admin Django
5.1 Crear el superuser con el comando python3 manage.py createsuperuser donde solicitará un correo y contraseña.
5.2 Creado el super usuario, ir a la ruta http://127.0.0.1:8000/admin/ y con el correo y contraseña ingresados en el paso 1, acceder al admin web de Django para administración de usuarios, posts y comments.