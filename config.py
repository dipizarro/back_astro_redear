import os
from typing import List

class Config:
    # Configuración de CORS
    CORS_ORIGINS: List[str] = [
        "https://astro-reader-mclsfc2uo-diegos-projects-5cd33d19.vercel.app",  # Tu frontend en Vercel
        "https://astro-reader.vercel.app",  # Dominio de producción (cuando lo tengas)
        "https://astro-reader-mclsfc2uo-diegos-projects-5cd33d19.vercel.app",  # Tu dominio actual
        "http://localhost:3000",  # Desarrollo local
        "http://localhost:5173",  # Vite dev server
        "http://localhost:8080",  # Otros puertos de desarrollo
    ]
    
    # Configuración de la aplicación
    APP_NAME: str = "Astro Reader API"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # Configuración de seguridad
    ALLOW_CREDENTIALS: bool = True
    ALLOW_METHODS: List[str] = ["GET", "POST", "OPTIONS"]
    ALLOW_HEADERS: List[str] = ["*"]

# Configuración para desarrollo
class DevelopmentConfig(Config):
    DEBUG = True
    CORS_ORIGINS = ["*"]  # Permitir todos los orígenes en desarrollo

# Configuración temporal para Render (permitir todos los orígenes)
class RenderConfig(Config):
    DEBUG = False
    CORS_ORIGINS = ["*"]  # Temporalmente permitir todos los orígenes

# Configuración para producción
class ProductionConfig(Config):
    DEBUG = False

# Función para obtener la configuración según el entorno
def get_config():
    env = os.getenv("ENVIRONMENT", "development")
    if env == "production":
        return ProductionConfig()
    elif env == "render":
        return RenderConfig()
    return DevelopmentConfig()
