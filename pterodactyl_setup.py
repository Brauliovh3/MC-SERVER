#!/usr/bin/env python3
"""Setup específico para Pterodactyl - Sin descarga automática"""

import os
import json
from config import SERVER_CONFIG, RULES

def create_pterodactyl_config():
    """Crea configuración para Pterodactyl"""
    
    # Crear directorio de configuración
    os.makedirs("config", exist_ok=True)
    
    # Guardar configuración del servidor
    with open("config/server_config.json", "w") as f:
        json.dump(SERVER_CONFIG, f, indent=2)
    
    # Crear archivo de reglas
    with open("config/rules.txt", "w", encoding="utf-8") as f:
        f.write("=== REGLAS DEL SERVIDOR BVH3_INDUSTRIES ===\n\n")
        for i, rule in enumerate(RULES, 1):
            f.write(f"{i}. {rule}\n")
    
    # Crear archivo de información
    with open("server_info.txt", "w", encoding="utf-8") as f:
        f.write(f"""
=== SERVIDOR BVH3_INDUSTRIES ===

Nombre: {SERVER_CONFIG['server_name']}
IP: {SERVER_CONFIG['server_ip']}
Puerto: {SERVER_CONFIG['server_port']}
Jugadores máximos: {SERVER_CONFIG['max_players']}
Modo de juego: {SERVER_CONFIG['gamemode']}
Dificultad: {SERVER_CONFIG['difficulty']}

INSTRUCCIONES PARA PTERODACTYL:
1. Sube manualmente los archivos del servidor Bedrock
2. Coloca bedrock_server.exe en la carpeta raíz
3. Configura los puertos en el panel de Pterodactyl
4. Reinicia el servidor

ARCHIVOS NECESARIOS:
- bedrock_server.exe (servidor principal)
- server.properties (configuración)
- allowlist.json (lista blanca)
- permissions.json (permisos)
""")
    
    print("✅ Configuración para Pterodactyl creada")
    print("📁 Archivos generados:")
    print("  - config/server_config.json")
    print("  - config/rules.txt") 
    print("  - server_info.txt")

if __name__ == "__main__":
    create_pterodactyl_config()