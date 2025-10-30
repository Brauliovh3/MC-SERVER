#!/usr/bin/env python3
"""Script de configuración completa del servidor"""

from server import BedrockServer
from config import SERVER_CONFIG, ADDONS, RULES
import os

def setup_server():
    """Configura el servidor completo"""
    server = BedrockServer()
    
    # Descargar servidor si no existe
    if not os.path.exists("server/bedrock_server.exe"):
        print("🔄 Descargando servidor...")
        server.download_server()
    
    # Configurar servidor
    print("⚙️ Configurando servidor...")
    server.configure(**SERVER_CONFIG)
    
    # Instalar addons
    if ADDONS:
        print("📦 Instalando addons...")
        for addon in ADDONS:
            if os.path.exists(addon):
                server.install_addon(addon)
            else:
                print(f"⚠️ Addon no encontrado: {addon}")
        
        server.activate_addons()
    
    # Crear archivo de reglas
    print("📋 Creando reglas del servidor...")
    with open("server/rules.txt", "w", encoding="utf-8") as f:
        f.write("=== REGLAS DEL SERVIDOR ===\n\n")
        for i, rule in enumerate(RULES, 1):
            f.write(f"{i}. {rule}\n")
    
    print("✅ Servidor configurado completamente")
    return server

if __name__ == "__main__":
    server = setup_server()
    
    print("\n🚀 Iniciando servidor...")
    server.start()