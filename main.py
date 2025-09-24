#!/usr/bin/env python3
# PiVoltMeter - Vereinfachte Hauptdatei
# Datum: 24.09.2025  
# Version: 2.0 - Vereinfacht mit JSON-Config

import time
import threading
from rpi_ws281x import PixelStrip, Color
from config.config import Config

def init_led_strips():
    """Initialisiert beide LED-Streifen"""
    print("🔌 Initialisiere LED-Streifen...")
    
    # Linker Strip
    left_strip = PixelStrip(
        Config.LEFT_STRIP_LEDS, 
        Config.LEFT_STRIP_PIN,
        Config.LED_FREQ_HZ, 
        Config.LED_DMA_LEFT, 
        Config.LED_INVERT, 
        Config.LED_BRIGHTNESS, 
        Config.LED_CHANNEL_LEFT
    )
    
    # Rechter Strip  
    right_strip = PixelStrip(
        Config.RIGHT_STRIP_LEDS, 
        Config.RIGHT_STRIP_PIN,
        Config.LED_FREQ_HZ, 
        Config.LED_DMA_RIGHT, 
        Config.LED_INVERT, 
        Config.LED_BRIGHTNESS, 
        Config.LED_CHANNEL_RIGHT
    )
    
    # Streifen starten
    left_strip.begin()
    right_strip.begin()
    
    print(f"✅ LEDs bereit: {Config.LEFT_STRIP_LEDS}L + {Config.RIGHT_STRIP_LEDS}R")
    return left_strip, right_strip

def startup_animation(left_strip, right_strip):
    """Einfache Start-Animation"""
    print("🌟 Starte LED-Animation...")
    
    colors = [
        Color(255, 0, 0),    # Rot
        Color(255, 255, 0),  # Gelb  
        Color(0, 255, 0),    # Grün
    ]
    
    # Alle LEDs durchlaufen alle Farben
    for color in colors:
        # Alle LEDs auf Farbe setzen
        for i in range(Config.LEFT_STRIP_LEDS):
            left_strip.setPixelColor(i, color)
        for i in range(Config.RIGHT_STRIP_LEDS):
            right_strip.setPixelColor(i, color)
            
        # Anzeigen
        left_strip.show()
        right_strip.show()
        time.sleep(0.5)
    
    # Alle LEDs ausschalten
    clear_leds(left_strip, right_strip)
    print("✅ Start-Animation abgeschlossen")

def clear_leds(left_strip, right_strip):
    """Schaltet alle LEDs aus"""
    for i in range(Config.LEFT_STRIP_LEDS):
        left_strip.setPixelColor(i, Color(0, 0, 0))
    for i in range(Config.RIGHT_STRIP_LEDS):
        right_strip.setPixelColor(i, Color(0, 0, 0))
    left_strip.show()
    right_strip.show()

def set_all_color(left_strip, right_strip, color_hex):
    """Setzt alle LEDs auf eine Farbe"""
    # Hex zu RGB konvertieren
    color_hex = color_hex.lstrip('#')
    r = int(color_hex[0:2], 16)
    g = int(color_hex[2:4], 16) 
    b = int(color_hex[4:6], 16)
    color = Color(r, g, b)
    
    # Alle LEDs setzen
    for i in range(Config.LEFT_STRIP_LEDS):
        left_strip.setPixelColor(i, color)
    for i in range(Config.RIGHT_STRIP_LEDS):
        right_strip.setPixelColor(i, color)
        
    left_strip.show()
    right_strip.show()
    print(f"🎨 Alle LEDs auf {color_hex}")

def audio_visualization_worker(left_strip, right_strip):
    """Audio-Visualisierung in separatem Thread (Platzhalter)"""
    print("🎵 Audio-Visualisierung startet...")
    
    # TODO: Hier kommt später led/audio_viz.py Import
    # Für jetzt: einfacher Platzhalter
    try:
        while True:
            # Placeholder für Audio-Visualisierung
            # Wird später durch led/audio_viz.py ersetzt
            time.sleep(1)
    except KeyboardInterrupt:
        print("🎵 Audio-Visualisierung beendet")
        clear_leds(left_strip, right_strip)

def start_flask_server():
    """Startet den Flask-Webserver"""
    try:
        print("🌐 Starte Web-Server...")
        # TODO: Wird später durch web/app.py ersetzt
        from web.app import app
        app.run(host='0.0.0.0', port=5000, threaded=True)
    except ImportError:
        # Fallback falls web/app.py noch nicht existiert
        print("⚠️  web/app.py nicht gefunden - verwende Fallback")
        try:
            from only_flask import start_flask_server as old_flask
            old_flask()
        except ImportError:
            print("❌ Kein Flask-Server verfügbar!")
            return False
    except Exception as e:
        print(f"❌ Fehler beim Starten des Web-Servers: {e}")
        return False

def main():
    """Hauptfunktion - Vereinfacht"""
    print("=" * 50)
    print("🚀 PiVoltMeter v2.0 - Vereinfacht")
    print("=" * 50)
    
    # Konfiguration anzeigen
    Config.print_config()
    
    try:
        # LED-Streifen initialisieren
        left_strip, right_strip = init_led_strips()
        
        # Start-Animation
        startup_animation(left_strip, right_strip)
        
        # LEDs auf gespeicherte Farbe setzen
        if Config.VISUALIZATION_MODE == 'static':
            set_all_color(left_strip, right_strip, Config.CURRENT_COLOR)
        
        # Audio-Visualisierung starten (falls aktiviert)
        if Config.VISUALIZATION_MODE == 'audio':
            audio_thread = threading.Thread(
                target=audio_visualization_worker, 
                args=(left_strip, right_strip),
                daemon=True
            )
            audio_thread.start()
            print("🎵 Audio-Thread gestartet")
        
        # Global verfügbar machen für Flask
        import builtins
        builtins.led_strips = (left_strip, right_strip)
        
        # Flask-Server starten (blockiert hier)
        print("🌐 Starte Flask-Server...")
        start_flask_server()
        
    except KeyboardInterrupt:
        print("\n🛑 Programm beendet durch Benutzer")
    except Exception as e:
        print(f"❌ Unerwarteter Fehler: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Aufräumen
        try:
            clear_leds(left_strip, right_strip)
            print("🧹 LEDs ausgeschaltet")
        except:
            pass
        
        print("👋 PiVoltMeter beendet")

if __name__ == "__main__":
    main()