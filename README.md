# Servidor Minecraft Bedrock con Addons

Servidor Bedrock programático con soporte completo para addons.

## Instalación

```bash
pip install requests
```

## Uso Básico

```python
python server.py
```

## Instalar Addons

```python
from server import BedrockServer

server = BedrockServer()
server.install_addon("mi_addon.mcpack")
server.activate_addons()
server.start()
```

## Configuración

Edita los parámetros en `server.py`:
- `server_name`: Nombre del servidor
- `max_players`: Jugadores máximos
- `gamemode`: survival, creative, adventure
- `difficulty`: peaceful, easy, normal, hard

## Estructura

```
bedrock_server/
├── server.py          # Script principal
├── server/            # Archivos del servidor
│   ├── behavior_packs/
│   ├── resource_packs/
│   └── worlds/
```

## Conectarse

- IP: 0.0.0.0 (todas las IPs) o tu IP específica
- Puerto: 19132 (configurable)
- IPv6: Puerto 19133

## Configuración de Red

Edita en `config.py`:
```python
"server_ip": "0.0.0.0",     # 0.0.0.0 para todas las IPs
"server_port": 19132,       # Puerto principal
"server_portv6": 19133      # Puerto IPv6
```
