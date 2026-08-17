#!/bin/bash

cd /home/ubuntu/02_backend_app_ipuc/

echo "DEPLOY SH -> ACTUALIZANDO SERVIDOR"

git pull origin main

docker compose up -d --build

echo "DEPLOY SH -> DESPLIEGUE FINALIZADO"