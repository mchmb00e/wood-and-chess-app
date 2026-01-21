¿Cómo iniciar el proyecto?

1. Ir a la carpeta sql/
2. Ejecutar el siguiente comando:
    mysql -u root -p < configure.sql
3. Si sql/backup/ contiene archivos, ejecutar el que tenga el indice mas alto:
    mysql -u root -p INGSWI_WOODCHESS < backup_i.sql
4. Crear un entorno de python 3 en la carpeta api/:
    python3 -m venv .venv
5. Activarlo:
    source .venv/bin/activate
6. Ejecutar en api/:
    pip install -r requirements.txt
7. Clonar el archivo env_template con el nombre .env y rellenar las variables faltantes, los valores serán dados por WhatsApp.
    cp env_template .env
8. Ejecutar:
    python3 run.py
9. Probar la API, buscar el siguiente enlace en un navegador:
    http://127.0.0.1:5000/


¿Cómo subir cambios a github?
Nota: .gitignore es un archivo que hará ignorar la basura y claves que pueden ser robadas.

1. Si realizaste cambios utiles a la base de datos, dirigirte a sql/backup:
    mysqldump -u root -p INGSWI_WOODCHESS > backup_i.sql
    Recuerda: i es el valor máximo + 1 de todos los backup.
2. Con el entorno activado, realizar:
    pip freeze > requirements.txt
3. Dirigirse a la raiz del proyecto.
4. Añadir las carpetas al commit:
    git add api/ sql/
5. Configurar el mensaje del commit:
    git commit -m "mensaje"
    Ejemplo: Si creaste un modulo X, entonces: git commit -m "create. X"
6. git push origin main