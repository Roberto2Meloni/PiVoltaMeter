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
import signal
import sys
import atexit

def cleanup(led_manager):
    try:
        print("Schalte LEDs aus...")
        led_manager.turn_off_leds()
    except Exception as e:
        print(f"Fehler beim Ausschalten der LEDs: {e}")

# Registrieren für normales Beenden
# atexit.register(cleanup)
led_manager = None  # Variable außerhalb der Funktion definieren


def signal_handler(sig, frame):
    print("Signal empfangen, beende Programm...")
    sys.exit(0)  # Dies wird atexit.register auslösen

# Signal-Handler registrieren
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def main():
    """Hauptfunktion des Programms"""
    try:
        print("Starte LED-Visualisierungssystem")
         # LED-Manager erstellen
        led_manager = LEDManager()
        
        # LED-Start-Animation
        only_led.start_all_start_phase()
        
        # Visualisierung starten
        led_manager.start_visualization()
        
        # Flask-Server mit LED-Manager starten
        start_flask_server(led_manager_instance=led_manager)

    except Exception as e:
        print(f"Unerwarteter Fehler: {e}")
    finally:
        cleanup(led_manager)  # Sicherheitshalber nochmal aufrufen

if __name__ == "__main__":
    main()