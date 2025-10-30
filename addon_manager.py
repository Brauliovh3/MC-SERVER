#!/usr/bin/env python3
"""Gestor de addons para servidor Bedrock"""

import os
import json
import zipfile
import shutil

class AddonManager:
    def __init__(self):
        self.behavior_packs_dir = "behavior_packs"
        self.resource_packs_dir = "resource_packs"
        self.worlds_dir = "worlds"
        
    def install_addon(self, addon_path):
        """Instala un addon (.mcpack, .mcaddon)"""
        if not os.path.exists(addon_path):
            print(f"❌ Addon no encontrado: {addon_path}")
            return False
            
        addon_name = os.path.splitext(os.path.basename(addon_path))[0]
        print(f"📦 Instalando addon: {addon_name}")
        
        try:
            with zipfile.ZipFile(addon_path, 'r') as zip_ref:
                files = zip_ref.namelist()
                
                if 'manifest.json' in files:
                    # Addon simple
                    manifest = json.loads(zip_ref.read('manifest.json'))
                    pack_type = manifest['modules'][0]['type']
                    
                    if pack_type == 'data':
                        target_dir = f"{self.behavior_packs_dir}/{addon_name}"
                    else:
                        target_dir = f"{self.resource_packs_dir}/{addon_name}"
                    
                    zip_ref.extractall(target_dir)
                    print(f"✅ {addon_name} instalado como {pack_type} pack")
                    
                else:
                    # Addon múltiple
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
                            
                            print(f"✅ {item} instalado como {pack_type} pack")
                    
                    shutil.rmtree("temp_addon")
            
            return True
            
        except Exception as e:
            print(f"❌ Error instalando {addon_name}: {e}")
            return False
    
    def activate_addons(self):
        """Activa todos los addons instalados"""
        world_path = f"{self.worlds_dir}/Bedrock level"
        os.makedirs(world_path, exist_ok=True)
        
        behavior_packs = []
        resource_packs = []
        
        # Escanear behavior packs
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
        
        # Escanear resource packs
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
        
        # Guardar configuración de packs
        if behavior_packs:
            with open(f"{world_path}/world_behavior_packs.json", "w") as f:
                json.dump(behavior_packs, f, indent=2)
        
        if resource_packs:
            with open(f"{world_path}/world_resource_packs.json", "w") as f:
                json.dump(resource_packs, f, indent=2)
        
        print(f"🎮 Activados: {len(behavior_packs)} behavior packs, {len(resource_packs)} resource packs")
        return len(behavior_packs) + len(resource_packs)

def main():
    """Instala addons desde la configuración"""
    from config import ADDONS
    
    manager = AddonManager()
    
    if ADDONS:
        print("📦 Instalando addons configurados...")
        for addon in ADDONS:
            manager.install_addon(addon)
        
        manager.activate_addons()
    else:
        print("📋 No hay addons configurados")
        print("💡 Agrega archivos .mcpack a la lista ADDONS en config.py")

if __name__ == "__main__":
    main()