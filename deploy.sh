#!/bin/bash

# Script para deployar en Google Cloud Run
# Asegúrate de tener gcloud CLI instalado y configurado

# Configuración
PROJECT_ID="tu-project-id"  # Reemplaza con tu Project ID
SERVICE_NAME="astro-reader-backend"
REGION="us-central1"  # Cambia la región según prefieras

echo "🚀 Iniciando deployment en Cloud Run..."

# Construir y subir la imagen
echo "📦 Construyendo imagen Docker..."
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME

# Deployar en Cloud Run
echo "🌐 Deployando en Cloud Run..."
gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --max-instances 10 \
  --timeout 300

echo "✅ Deployment completado!"
echo "🌍 Tu API estará disponible en:"
gcloud run services describe $SERVICE_NAME --region $REGION --format="value(status.url)"
