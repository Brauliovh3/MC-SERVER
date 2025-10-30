import subprocess
import os
import urllib.request
import zipfile
import json
import shutil

class BedrockServer:
    def __init__(self, server_dir="server"):
        self.server_dir = server_dir
        self.behavior_packs_dir = f"{server_dir}/behavior_packs"
        self.resource_packs_dir = f"{server_dir}/resource_packs"
        self.worlds_dir = f"{server_dir}/worlds"
        
    def download_server(self):
        """Descarga servidor Bedrock oficial"""
        url = "https://minecraft.azureedge.net/bin-win/bedrock-server-1.20.81.01.zip"
        zip_path = "bedrock-server.zip"
        
        print("Descargando servidor...")
        urllib.request.urlretrieve(url, zip_path)
        
        os.makedirs(self.server_dir, exist_ok=True)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(self.server_dir)
        
        os.remove(zip_path)
        print("✓ Servidor descargado")
    
    def configure(self, server_name="Servidor Bedrock", max_players=10, gamemode="survival", difficulty="normal", allow_cheats=False, view_distance=32, player_idle_timeout=30, default_player_permission="member", server_ip="0.0.0.0", server_port=19132, server_portv6=19133):
        """Configura el servidor"""
        config = f"""server-name={server_name}
gamemode={gamemode}
difficulty={difficulty}
max-players={max_players}
online-mode=true
allow-cheats={str(allow_cheats).lower()}
view-distance={view_distance}
tick-distance=4
player-idle-timeout={player_idle_timeout}
max-threads=8
level-name=Bedrock level
level-seed=
default-player-permission-level={default_player_permission}
texturepack-required=false
server-port={server_port}
server-portv6={server_portv6}
server-ip={server_ip}
"""
        with open(f"{self.server_dir}/server.properties", "w") as f:
            f.write(config)
        print("✓ Servidor configurado")
    
    def install_addon(self, addon_path):
        """Instala un addon (.mcpack, .mcaddon o .zip)"""
        os.makedirs(self.behavior_packs_dir, exist_ok=True)
        os.makedirs(self.resource_packs_dir, exist_ok=True)
        
        addon_name = os.path.splitext(os.path.basename(addon_path))[0]
        
        with zipfile.ZipFile(addon_path, 'r') as zip_ref:
            files = zip_ref.namelist()
            
            if 'manifest.json' in files:
                manifest = json.loads(zip_ref.read('manifest.json'))
                pack_type = manifest['modules'][0]['type']
                
                if pack_type == 'data':
                    target_dir = f"{self.behavior_packs_dir}/{addon_name}"
                else:
                    target_dir = f"{self.resource_packs_dir}/{addon_name}"
                
                zip_ref.extractall(target_dir)
                print(f"✓ Addon instalado: {addon_name}")
            else:
                zip_ref.extractall("temp_addon")
                
                for item in os.listdir("temp_addon"):
                    item_path = f"temp_addon/{item}"
                    if os.path.isdir(item_path) and os.path.exists(f"{item_path}/manifest.json"):
                        with open(f"{item_path}/manifest.json") as f:
                            manifest = json.load(f)
                        
                        pack_type = manifest['modules'][0]['type']
                        if pack_type == 'data':
                            shutil.move(item_path, f"{self.behavior_packs_dir}/{item}")
                        else:
                            shutil.move(item_path, f"{self.resource_packs_dir}/{item}")
                
                shutil.rmtree("temp_addon")
                print(f"✓ Addon instalado: {addon_name}")
    
    def activate_addons(self):
        """Activa todos los addons instalados"""
        world_path = f"{self.worlds_dir}/Bedrock level"
        
        behavior_packs = []
        resource_packs = []
        
        if os.path.exists(self.behavior_packs_dir):
            for pack in os.listdir(self.behavior_packs_dir):
                manifest_path = f"{self.behavior_packs_dir}/{pack}/manifest.json"
                if os.path.exists(manifest_path):
                    with open(manifest_path) as f:
                        manifest = json.load(f)
                    behavior_packs.append({
                        "pack_id": manifest['header']['uuid'],
                        "version": manifest['header']['version']
                    })
        
        if os.path.exists(self.resource_packs_dir):
            for pack in os.listdir(self.resource_packs_dir):
                manifest_path = f"{self.resource_packs_dir}/{pack}/manifest.json"
                if os.path.exists(manifest_path):
                    with open(manifest_path) as f:
                        manifest = json.load(f)
                    resource_packs.append({
                        "pack_id": manifest['header']['uuid'],
                        "version": manifest['header']['version']
                    })
        
        if behavior_packs:
            os.makedirs(world_path, exist_ok=True)
            with open(f"{world_path}/world_behavior_packs.json", "w") as f:
                json.dump(behavior_packs, f, indent=2)
        
        if resource_packs:
            os.makedirs(world_path, exist_ok=True)
            with open(f"{world_path}/world_resource_packs.json", "w") as f:
                json.dump(resource_packs, f, indent=2)
        
        print(f"✓ Activados {len(behavior_packs)} behavior packs y {len(resource_packs)} resource packs")
    
    def start(self):
        """Inicia el servidor"""
        print("\n=== Iniciando servidor ===")
        exe = f"{self.server_dir}/bedrock_server.exe"
        subprocess.run([exe], cwd=self.server_dir)

if __name__ == "__main__":
    server = BedrockServer()
    
    if not os.path.exists("server/bedrock_server.exe"):
        server.download_server()
        server.configure(
            server_name="Mi Servidor Bedrock",
            max_players=20,
            gamemode="survival"
        )
    
    # server.install_addon("mi_addon.mcpack")
    # server.activate_addons()
    
    server.start()
