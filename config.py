# Configuración del servidor
SERVER_CONFIG = {
    "server_name": "BVH3_INDUSTRIES",
    "max_players": 20,
    "gamemode": "survival",  # survival, creative, adventure
    "difficulty": "normal",  # peaceful, easy, normal, hard
    "allow_cheats": False,
    "view_distance": 32,
    "player_idle_timeout": 30,
    "default_player_permission": "member",  # visitor, member, operator
    "server_ip": "bvh3industries.ddns.net",  # Dominio personalizado
    "server_port": 19132,
    "server_portv6": 19133
}

# Addons a instalar (coloca los archivos .mcpack en la carpeta)
ADDONS = [
    # "addon1.mcpack",
    # "addon2.mcpack"
]

# Reglas del servidor
RULES = [
    "No griefing",
    "Respeta a otros jugadores", 
    "No spam en el chat",
    "No usar hacks o cheats"
]