#!/usr/bin/env python3
"""Servidor Bedrock real con detección de jugadores"""

import os
import sys
import subprocess
import threading
import time
import re
from config import SERVER_CONFIG

class BedrockServerManager:
    def __init__(self):
        self.players = set()
        self.server_process = None
        
    def monitor_logs(self, process):
        """Monitorea logs del servidor en tiempo real"""
        for line in iter(process.stdout.readline, b''):
            log_line = line.decode('utf-8', errors='ignore').strip()
            if log_line:
                print(f"[SERVER] {log_line}")
                self.parse_player_events(log_line)
    
    def parse_player_events(self, log_line):
        """Detecta eventos de jugadores en los logs"""
        # Jugador se conecta
        connect_match = re.search(r'Player connected: (.+?),', log_line)
        if connect_match:
            player = connect_match.group(1)
            self.players.add(player)
            print(f"🟢 JUGADOR CONECTADO: {player} | Total: {len(self.players)}")
        
        # Jugador se desconecta
        disconnect_match = re.search(r'Player disconnected: (.+?),', log_line)
        if disconnect_match:
            player = disconnect_match.group(1)
            self.players.discard(player)
            print(f"🔴 JUGADOR DESCONECTADO: {player} | Total: {len(self.players)}")
    
    def start_bedrock_server(self):
        """Inicia el servidor Bedrock oficial"""
        if not os.path.exists("bedrock_server"):
            print("❌ Servidor Bedrock no encontrado")
            print("📥 Descargando servidor...")
            self.download_server()
        
        print("🚀 Iniciando BVH3_INDUSTRIES Bedrock Server")
        print(f"📍 IP: {SERVER_CONFIG['server_ip']}:{SERVER_CONFIG['server_port']}")
        print(f"👥 Máximo: {SERVER_CONFIG['max_players']} jugadores")
        print(f"🎮 Modo: {SERVER_CONFIG['gamemode']}")
        print("\n" + "="*50)
        
        try:
            # Ejecutar servidor Bedrock
            self.server_process = subprocess.Popen(
                ["./bedrock_server"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=False,
                bufsize=1
            )
            
            # Monitor de logs en hilo separado
            log_thread = threading.Thread(target=self.monitor_logs, args=(self.server_process,))
            log_thread.daemon = True
            log_thread.start()
            
            # Esperar a que termine el servidor
            self.server_process.wait()
            
        except FileNotFoundError:
            print("❌ bedrock_server no encontrado")
            print("📋 Instrucciones:")
            print("1. Descarga Bedrock Server de minecraft.net")
            print("2. Extrae bedrock_server en la carpeta raíz")
            print("3. Reinicia el servidor")
            self.simulate_server()
        except KeyboardInterrupt:
            print("\n🛑 Deteniendo servidor...")
            if self.server_process:
                self.server_process.terminate()
    
    def download_server(self):
        """Intenta descargar el servidor Bedrock"""
        try:
            import urllib.request
            import zipfile
            
            url = "https://minecraft.azureedge.net/bin-linux/bedrock-server-1.20.81.01.zip"
            print("📥 Descargando servidor Bedrock...")
            urllib.request.urlretrieve(url, "bedrock-server.zip")
            
            with zipfile.ZipFile("bedrock-server.zip", 'r') as zip_ref:
                zip_ref.extractall(".")
            
            os.remove("bedrock-server.zip")
            os.chmod("bedrock_server", 0o755)
            print("✅ Servidor descargado")
            
        except Exception as e:
            print(f"❌ Error descargando: {e}")
            print("📋 Descarga manual requerida")
    
    def simulate_server(self):
        """Servidor simulado con eventos de jugadores"""
        print("\n🔄 Modo simulación activado")
        print("👥 Simulando conexiones de jugadores...")
        
        fake_players = ["Steve", "Alex", "Notch", "Herobrine", "CaptainSparklez"]
        
        try:
            while True:
                time.sleep(30)
                
                # Simular conexión aleatoria
                if len(self.players) < 3 and time.time() % 60 < 30:
                    import random
                    new_player = random.choice([p for p in fake_players if p not in self.players])
                    if new_player:
                        self.players.add(new_player)
                        print(f"🟢 JUGADOR CONECTADO: {new_player} | Total: {len(self.players)}")
                
                # Simular desconexión
                elif self.players and time.time() % 90 < 30:
                    import random
                    leaving_player = random.choice(list(self.players))
                    self.players.remove(leaving_player)
                    print(f"🔴 JUGADOR DESCONECTADO: {leaving_player} | Total: {len(self.players)}")
                
                print(f"⏰ Servidor activo - {time.strftime('%H:%M:%S')} | Jugadores: {len(self.players)}")
                
        except KeyboardInterrupt:
            print("\n🛑 Servidor detenido")

def main():
    server = BedrockServerManager()
    server.start_bedrock_server()

if __name__ == "__main__":
    main()