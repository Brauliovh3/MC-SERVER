#!/usr/bin/env python3
"""Archivo principal para Pterodactyl Panel"""

import os
import sys
from setup import setup_server

def main():
    """Función principal para Pterodactyl"""
    print("🚀 Iniciando BVH3_INDUSTRIES en Pterodactyl...")
    
    # Configurar servidor automáticamente
    server = setup_server()
    
    # Iniciar servidor
    server.start()

if __name__ == "__main__":
    main()