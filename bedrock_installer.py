#!/usr/bin/env python3
"""Instalador automático del servidor Bedrock para Pterodactyl"""

import os
import urllib.request
import zipfile
import json
from config import SERVER_CONFIG, ADDONS, RULES

def install_bedrock_server():
    """Instala y configura el servidor Bedrock"""
    
    print("🚀 Instalando BVH3_INDUSTRIES Bedrock Server...")
    
    # Descargar servidor Bedrock para Linux
    if not os.path.exists("bedrock_server"):
        try:
            url = "https://minecraft.azureedge.net/bin-linux/bedrock-server-1.20.81.01.zip"
            print("📥 Descargando servidor Bedrock...")
            urllib.request.urlretrieve(url, "bedrock-server.zip")
            
            with zipfile.ZipFile("bedrock-server.zip", 'r') as zip_ref:
                zip_ref.extractall(".")
            
            os.remove("bedrock-server.zip")
            os.chmod("bedrock_server", 0o755)
            print("✅ Servidor Bedrock instalado")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    # Configurar server.properties
    config_content = f"""server-name={SERVER_CONFIG['server_name']}
gamemode={SERVER_CONFIG['gamemode']}
difficulty={SERVER_CONFIG['difficulty']}
max-players={SERVER_CONFIG['max_players']}
online-mode=true
allow-cheats={str(SERVER_CONFIG['allow_cheats']).lower()}
view-distance={SERVER_CONFIG['view_distance']}
tick-distance=4
player-idle-timeout={SERVER_CONFIG['player_idle_timeout']}
max-threads=8
level-name=Bedrock level
level-seed=
default-player-permission-level={SERVER_CONFIG['default_player_permission']}
texturepack-required=false
server-port={SERVER_CONFIG['server_port']}
server-portv6={SERVER_CONFIG['server_portv6']}
"""
    
    with open("server.properties", "w") as f:
        f.write(config_content)
    print("⚙️ Configuración aplicada")
    
    # Crear directorios para addons
    os.makedirs("behavior_packs", exist_ok=True)
    os.makedirs("resource_packs", exist_ok=True)
    os.makedirs("worlds", exist_ok=True)
    
    # Crear archivo de reglas
    with open("rules.txt", "w", encoding="utf-8") as f:
        f.write("=== REGLAS BVH3_INDUSTRIES ===\n\n")
        for i, rule in enumerate(RULES, 1):
            f.write(f"{i}. {rule}\n")
    
    print("📋 Reglas del servidor creadas")
    print("✅ Instalación completa")
    
    return True

if __name__ == "__main__":
    install_bedrock_server()