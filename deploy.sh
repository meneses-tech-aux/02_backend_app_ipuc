#!/bin/bash

cd /home/ubuntu/02_backend_app_ipuc/

echo "DEPLOY SH -> ACTUALIZANDO SERVIDOR"

git pull origin main

sudo docker compose --env-file .env.development -f docker-compose.dev.yml up -d

echo "DEPLOY SH -> DESPLIEGUE FINALIZADO"