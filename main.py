# Datum:        08.04.2025
# Version:      1.0
# Beschreibung: Steuerung von WS2812b LEDs mit einem Raspberry Pi
# Releas Notes
# Version               Notes
# 1.0                   Erste Implementierung

# Datum:        11.04.2025
# Version:      1.0
# Beschreibung: Modulare LED-Visualisierung mit Audio- und Muster-Unterstützung

import threading
from config.config import Config
from utils.led_manager import LEDManager
from only_flask import start_flask_server
import only_led

def main():
    """Hauptfunktion des Programms"""
    print("Starte LED-Visualisierungssystem")
    
    # LED-Start-Animation
    only_led.start_all_start_phase()
    
    # LED-Manager erstellen
    led_manager = LEDManager()
    
    # Visualisierung starten
    led_manager.start_visualization()
    
    # Flask-Server mit LED-Manager starten
    start_flask_server(led_manager_instance=led_manager)

if __name__ == "__main__":
    main()