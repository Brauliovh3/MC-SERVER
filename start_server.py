#!/usr/bin/env python3
"""Script para iniciar el servidor en producción"""

import os
import sys
from server import BedrockServer

def start_production_server():
    """Inicia el servidor en modo producción"""
    
    # Verificar que el servidor esté configurado
    if not os.path.exists("server/bedrock_server.exe"):
        print("❌ Servidor no configurado. Ejecuta: python setup.py")
        sys.exit(1)
    
    if not os.path.exists("server/server.properties"):
        print("❌ Configuración no encontrada. Ejecuta: python setup.py")
        sys.exit(1)
    
    # Leer configuración actual
    config_lines = {}
    if os.path.exists("server/server.properties"):
        with open("server/server.properties", "r") as f:
            for line in f:
                if "=" in line:
                    key, value = line.strip().split("=", 1)
                    config_lines[key] = value
    
    server_ip = config_lines.get("server-ip", "0.0.0.0")
    server_port = config_lines.get("server-port", "19132")
    
    print("🌐 Iniciando servidor en producción...")
    print(f"📍 IP: {server_ip} (0.0.0.0 = todas las IPs)")
    print(f"🔌 Puerto: {server_port}")
    print("📋 Reglas en: server/rules.txt")
    print("\n" + "="*50)
    
    server = BedrockServer()
    server.start()

if __name__ == "__main__":
    start_production_server()