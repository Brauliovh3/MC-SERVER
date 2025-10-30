#!/usr/bin/env python3
"""Archivo principal para Pterodactyl Panel"""

import os
import sys
import time

def main():
    """Función principal para Pterodactyl"""
    print("🚀 BVH3_INDUSTRIES - Servidor Minecraft Bedrock")
    print("📍 IP: bvh3industries.ddns.net:19132")
    print("👥 Jugadores máximos: 20")
    print("🎮 Modo: Survival")
    print("\n⚠️  NOTA: Este es un servidor Python simulado para Pterodactyl")
    print("📋 Para servidor real, sube los archivos de Bedrock manualmente")
    
    # Mantener el proceso activo
    print("\n🔄 Servidor iniciado y funcionando...")
    try:
        while True:
            time.sleep(60)
            print(f"⏰ Servidor activo - {time.strftime('%H:%M:%S')}")
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido")

if __name__ == "__main__":
    main()