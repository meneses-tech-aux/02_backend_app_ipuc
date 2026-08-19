#!/bin/bash

echo "DEPLOY SH -> ACTUALIZANDO SERVIDOR"

# 1. Entrar a la carpeta del proyecto en el servidor
cd /home/ubuntu/02_backend_app_ipuc/

# 2. Traer el último código de GitHub
git pull origin main

# 3. Levantar los contenedores FORZANDO la reconstrucción de la imagen de la API
sudo docker compose --env-file .env.development -f docker-compose.dev.yml up -d --build --force-recreate

# 4. Limpiar imágenes viejas para que tu servidor AWS no se quede sin espacio de disco con el tiempo
sudo docker image prune -f

echo "DEPLOY SH -> DESPLIEGUE FINALIZADO"