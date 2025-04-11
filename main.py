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
from led_controllers.audio_visualizer import AudioVisualizer
from led_controllers.pattern_visualizer import PatternVisualizer
from only_flask import start_flask_server

def main():
    """Hauptfunktion des Programms"""
    print("Starte LED-Visualisierungssystem")
    
    # LED-Start-Animation (kann später in eine separate Funktion ausgelagert werden)
    from only_led import start_all_start_phase
    start_all_start_phase()

    # Visualisierungsmodus basierend auf Konfiguration wählen
    if Config.VISUALIZATION_MODE == 'audio':
        visualizer = AudioVisualizer()
        # Starte Audio-Visualisierung in einem separaten Thread
        audio_thread = threading.Thread(target=visualizer.start_visualization)
        audio_thread.daemon = True
        audio_thread.start()
    elif Config.VISUALIZATION_MODE == 'pattern':
        visualizer = PatternVisualizer()
        # Starte Muster-Visualisierung in einem separaten Thread
        pattern_thread = threading.Thread(target=visualizer.start_pattern)
        pattern_thread.daemon = True
        pattern_thread.start()

    # Starte Flask-Webserver
    start_flask_server()

if __name__ == "__main__":
    main()