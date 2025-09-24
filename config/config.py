# Minimalistische Konfiguration für PiVoltMeter LED-Steuerung
# Nur Werte die LED-Darstellung beeinflussen werden in JSON gespeichert
# Datum: 24.09.2025
# Version: 2.0

import json
import os
import socket
from datetime import datetime
from pathlib import Path

class Config:
    """Zentrale Konfiguration - Nur LED-relevante Werte persistent"""
    
    # Pfad zur Konfigurations-JSON
    CONFIG_FILE = Path(__file__).parent / "config.json"
    
    # ========================================
    # HARDWARE-SETTINGS (bleiben hardcoded)
    # ========================================
    LEFT_STRIP_PIN = 18         # GPIO Pin links
    RIGHT_STRIP_PIN = 13        # GPIO Pin rechts
    LED_FREQ_HZ = 800000        # Signal-Frequenz
    LED_DMA_LEFT = 10           # DMA Kanal links
    LED_DMA_RIGHT = 11          # DMA Kanal rechts
    LED_INVERT = False          # Signal invertieren
    LED_CHANNEL_LEFT = 0        # PWM Kanal links
    LED_CHANNEL_RIGHT = 1       # PWM Kanal rechts
    AUDIO_RATE = 44100          # Audio Sample Rate
    AUDIO_CHUNK = 1024          # Audio Buffer
    
    # ========================================
    # PERSISTENTE WERTE (werden in JSON gespeichert)
    # ========================================
    LEFT_STRIP_LEDS = 10        # Anzahl LEDs links
    RIGHT_STRIP_LEDS = 10       # Anzahl LEDs rechts
    VISUALIZATION_MODE = 'audio' # Aktueller Modus
    AUDIO_CHANNELS = 1          # Audio Kanäle
    
    LED_BRIGHTNESS = 50         # Helligkeit
    CURRENT_COLOR = '#00FF00'   # Aktuelle Farbe
    CURRENT_PATTERN = 'rainbow' # Aktuelles Muster
    
    AUDIO_SMOOTHING = 0.3       # Audio Glättung
    AMPLITUDE_COLOR_MODE = 'gradient'  # 'gradient' oder 'fixed'
    FIXED_AMPLITUDE_COLOR = '#00FF00'  # Farbe für Audio-Amplituden
    
    # ========================================
    # JSON LADEN/SPEICHERN
    # ========================================
    @classmethod
    def load_from_json(cls):
        """Lädt nur die LED-relevanten Werte aus JSON"""
        if not cls.CONFIG_FILE.exists():
            print(f"📄 Erstelle neue config.json...")
            cls.save_to_json()
            return
            
        try:
            with open(cls.CONFIG_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Lade die Werte (genau wie in deiner JSON-Struktur)
            cls.LEFT_STRIP_LEDS = data.get('left_strip_leds', cls.LEFT_STRIP_LEDS)
            cls.RIGHT_STRIP_LEDS = data.get('right_strip_leds', cls.RIGHT_STRIP_LEDS)
            cls.VISUALIZATION_MODE = data.get('visualization_mode', cls.VISUALIZATION_MODE)
            cls.AUDIO_CHANNELS = data.get('audio_channels', cls.AUDIO_CHANNELS)
            
            cls.LED_BRIGHTNESS = data.get('led_brightness', cls.LED_BRIGHTNESS)
            cls.CURRENT_COLOR = data.get('current_color', cls.CURRENT_COLOR)
            cls.CURRENT_PATTERN = data.get('current_pattern', cls.CURRENT_PATTERN)
            
            cls.AUDIO_SMOOTHING = data.get('audio_smoothing', cls.AUDIO_SMOOTHING)
            cls.AMPLITUDE_COLOR_MODE = data.get('amplitude_color_mode', cls.AMPLITUDE_COLOR_MODE)
            cls.FIXED_AMPLITUDE_COLOR = data.get('fixed_amplitude_color', cls.FIXED_AMPLITUDE_COLOR)
            
            print(f"✅ Config geladen: {cls.LEFT_STRIP_LEDS}L + {cls.RIGHT_STRIP_LEDS}R LEDs")
            
        except Exception as e:
            print(f"⚠️  Fehler beim Laden: {e}")
            print("📄 Verwende Standard-Werte...")
    
    @classmethod
    def save_to_json(cls):
        """Speichert nur die LED-relevanten Werte in JSON"""
        try:
            # Erstelle Ordner falls nicht vorhanden
            cls.CONFIG_FILE.parent.mkdir(exist_ok=True)
            
            # Minimale JSON-Struktur (wie deine Vorlage)
            data = {
                "left_strip_leds": cls.LEFT_STRIP_LEDS,
                "right_strip_leds": cls.RIGHT_STRIP_LEDS,
                "visualization_mode": cls.VISUALIZATION_MODE,
                "audio_channels": cls.AUDIO_CHANNELS,
                
                "led_brightness": cls.LED_BRIGHTNESS,
                "current_color": cls.CURRENT_COLOR,
                "current_pattern": cls.CURRENT_PATTERN,
                
                "audio_smoothing": cls.AUDIO_SMOOTHING,
                "amplitude_color_mode": cls.AMPLITUDE_COLOR_MODE,
                "fixed_amplitude_color": cls.FIXED_AMPLITUDE_COLOR
            }
            
            with open(cls.CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Konfiguration gespeichert")
            
        except Exception as e:
            print(f"❌ Fehler beim Speichern der config.json: {e}")
    
    # ========================================
    # SETTER-METHODEN (speichern automatisch)
    # ========================================
    @classmethod
    def set_left_strip_leds(cls, count):
        """Ändert Anzahl LEDs für linken Strip"""
        if 1 <= count <= 300:
            cls.LEFT_STRIP_LEDS = count
            cls.save_to_json()
            print(f"🎛️  Linker Strip: {count} LEDs")
        else:
            raise ValueError(f"LED-Anzahl muss zwischen 1 und 300 sein!")
    
    @classmethod
    def set_right_strip_leds(cls, count):
        """Ändert Anzahl LEDs für rechten Strip"""
        if 1 <= count <= 300:
            cls.RIGHT_STRIP_LEDS = count
            cls.save_to_json()
            print(f"🎛️  Rechter Strip: {count} LEDs")
        else:
            raise ValueError(f"LED-Anzahl muss zwischen 1 und 300 sein!")
    
    @classmethod
    def set_visualization_mode(cls, mode):
        """Ändert Visualisierungsmodus"""
        valid_modes = ['audio', 'pattern', 'static']
        if mode in valid_modes:
            cls.VISUALIZATION_MODE = mode
            cls.save_to_json()
            print(f"🎨 Modus: {mode}")
        else:
            raise ValueError(f"Modus muss einer von {valid_modes} sein!")
    
    @classmethod
    def set_current_color(cls, color):
        """Setzt aktuelle Farbe"""
        if color.startswith('#') and len(color) == 7:
            cls.CURRENT_COLOR = color
            cls.save_to_json()
            print(f"🎨 Farbe: {color}")
        else:
            raise ValueError(f"Farbe muss Format '#RRGGBB' haben!")
    
    @classmethod
    def set_amplitude_color(cls, color):
        """Setzt Audio-Amplituden-Farbe"""
        if color.startswith('#') and len(color) == 7:
            cls.FIXED_AMPLITUDE_COLOR = color
            cls.AMPLITUDE_COLOR_MODE = 'fixed'
            cls.save_to_json()
            print(f"🎵 Audio-Farbe: {color}")
        else:
            raise ValueError(f"Farbe muss Format '#RRGGBB' haben!")
    
    @classmethod
    def set_brightness(cls, brightness):
        """Setzt LED-Helligkeit"""
        if 0 <= brightness <= 255:
            cls.LED_BRIGHTNESS = brightness
            cls.save_to_json()
            print(f"💡 Helligkeit: {brightness}/255")
        else:
            raise ValueError(f"Helligkeit muss zwischen 0 und 255 sein!")
    
    # ========================================
    # QUICK-CONFIGS
    # ========================================
    @classmethod
    def quick_equal_strips(cls, count=10):
        """Beide Strips gleich groß"""
        cls.LEFT_STRIP_LEDS = count
        cls.RIGHT_STRIP_LEDS = count
        cls.save_to_json()
        print(f"✅ Beide Strips: {count} LEDs")
    
    @classmethod
    def quick_different_strips(cls, left=12, right=8):
        """Verschiedene Strip-Größen"""
        cls.LEFT_STRIP_LEDS = left
        cls.RIGHT_STRIP_LEDS = right
        cls.save_to_json()
        print(f"✅ Links: {left} LEDs, Rechts: {right} LEDs")
    
    # ========================================
    # INFO & DEBUG
    # ========================================
    @classmethod
    def print_config(cls):
        """Zeigt aktuelle Konfiguration"""
        print("=" * 50)
        print("🎛️  PiVoltMeter Konfiguration")
        print("=" * 50)
        print(f"📍 Linker Strip:  {cls.LEFT_STRIP_LEDS} LEDs an GPIO {cls.LEFT_STRIP_PIN}")
        print(f"📍 Rechter Strip: {cls.RIGHT_STRIP_LEDS} LEDs an GPIO {cls.RIGHT_STRIP_PIN}")
        print(f"💡 Helligkeit:    {cls.LED_BRIGHTNESS}/255")
        print(f"🎨 Modus:         {cls.VISUALIZATION_MODE}")
        print(f"🎨 Farbe:         {cls.CURRENT_COLOR}")
        print(f"🎵 Audio-Farbe:   {cls.FIXED_AMPLITUDE_COLOR} ({cls.AMPLITUDE_COLOR_MODE})")
        print(f"📂 Config-Datei:  {cls.CONFIG_FILE}")
        print("=" * 50)
    
    @classmethod
    def get_max_leds(cls):
        """Größere der beiden Strip-Größen"""
        return max(cls.LEFT_STRIP_LEDS, cls.RIGHT_STRIP_LEDS)
    
    @classmethod
    def get_ip_addresses(cls):
        """Ermittelt alle verfügbaren IP-Adressen des Pi"""
        ip_addresses = []
        try:
            import subprocess
            # Alle aktiven Netzwerk-Interfaces abfragen
            result = subprocess.run(['hostname', '-I'], capture_output=True, text=True)
            if result.returncode == 0:
                # Alle IPs aus der Ausgabe extrahieren
                ips = result.stdout.strip().split()
                for ip in ips:
                    if ip and not ip.startswith('127.'):  # Localhost ausschließen
                        ip_addresses.append(ip)
            
            # Fallback: Socket-Methode
            if not ip_addresses:
                try:
                    # Verbindung zu externem Server simulieren um lokale IP zu finden
                    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                        s.connect(("8.8.8.8", 80))  # Google DNS
                        local_ip = s.getsockname()[0]
                        if local_ip and local_ip != '127.0.0.1':
                            ip_addresses.append(local_ip)
                except:
                    pass
                    
        except Exception as e:
            print(f"⚠️  IP-Adress-Erkennung fehlgeschlagen: {e}")
            
        # Standard-Fallback
        if not ip_addresses:
            ip_addresses = ["192.168.x.x"]
            
        return ip_addresses

    @classmethod
    def to_json(cls):
        """Gibt aktuelle Konfiguration als Dictionary zurück (für Templates)"""
        try:
            return {
                "left_strip_leds": cls.LEFT_STRIP_LEDS,
                "right_strip_leds": cls.RIGHT_STRIP_LEDS,
                "visualization_mode": cls.VISUALIZATION_MODE,
                "audio_channels": cls.AUDIO_CHANNELS,
                "led_brightness": cls.LED_BRIGHTNESS,
                "current_color": cls.CURRENT_COLOR,
                "current_pattern": cls.CURRENT_PATTERN,
                "audio_smoothing": float(cls.AUDIO_SMOOTHING),  # Sicherstellen dass es float ist
                "amplitude_color_mode": cls.AMPLITUDE_COLOR_MODE,
                "fixed_amplitude_color": cls.FIXED_AMPLITUDE_COLOR,
                
                # Zusätzliche nützliche Werte für Templates
                "max_leds": cls.get_max_leds(),
                "total_leds": cls.LEFT_STRIP_LEDS + cls.RIGHT_STRIP_LEDS,
                "different_strip_sizes": cls.LEFT_STRIP_LEDS != cls.RIGHT_STRIP_LEDS,
                
                # Hardware-Info (nur für Anzeige)
                "left_strip_pin": cls.LEFT_STRIP_PIN,
                "right_strip_pin": cls.RIGHT_STRIP_PIN,
                
                # JavaScript-kompatible Werte (für altes Template)
                "led_color": cls._get_color_name_from_hex(cls.CURRENT_COLOR),
                "audio_pattern": cls._get_current_audio_pattern(),
                "static_pattern": cls._get_current_static_pattern(),
                
                # Display-Informationen für HTML-Template
                "display": {
                    "ip_addresses": cls.get_ip_addresses(),
                    "hostname": socket.gethostname(),
                    "port": 5000,
                    # JavaScript erwartet diese Namen für UI-Updates
                    "mode_name": cls._get_mode_display_name(),
                    "color_name": cls._get_color_display_name(),
                    "pattern_name": cls._get_pattern_display_name()
                }
            }
        except Exception as e:
            print(f"⚠️  Fehler bei to_json(): {e}")
            # Fallback - minimal dictionary
            return {
                "left_strip_leds": 10,
                "right_strip_leds": 10,
                "visualization_mode": "audio",
                "current_color": "#00FF00",
                "led_brightness": 50,
                "led_color": "green",
                "audio_pattern": "audio_pattern_01",
                "static_pattern": "static_pattern_01",
                "display": {
                    "ip_addresses": ["192.168.x.x"],
                    "hostname": "raspberrypi",
                    "port": 5000,
                    "mode_name": "Audio",
                    "color_name": "Grün", 
                    "pattern_name": "Spektrum"
                }
            }
    
    @classmethod
    def _get_color_name_from_hex(cls, hex_color):
        """Konvertiert Hex-Farbe zu Namen für JavaScript"""
        color_map = {
            "#00FF00": "green",
            "#FF0000": "red", 
            "#0000FF": "blue",
            "#FFFF00": "yellow",
            "#FF00FF": "purple",
            "#00FFFF": "cyan",
            "rainbow": "rainbow"
        }
        return color_map.get(hex_color, "green")
    
    @classmethod
    def _get_current_audio_pattern(cls):
        """Gibt aktuelles Audio-Pattern für JavaScript zurück"""
        # Standard Audio-Pattern basierend auf Config
        return "audio_pattern_01"  # Kann später erweitert werden
    
    @classmethod
    def _get_current_static_pattern(cls):
        """Gibt aktuelles Static-Pattern für JavaScript zurück"""
        # Standard Static-Pattern basierend auf Config
        return "static_pattern_01"  # Kann später erweitert werden
    
    @classmethod
    def _get_mode_display_name(cls):
        """Gibt benutzerfreundlichen Namen für Visualisierungsmodus zurück"""
        mode_names = {
            "audio": "Audio",
            "static": "Statisch", 
            "pattern": "Muster",
            "off": "Aus"
        }
        return mode_names.get(cls.VISUALIZATION_MODE, "Audio")
    
    @classmethod
    def _get_color_display_name(cls):
        """Gibt benutzerfreundlichen Namen für Farbe zurück"""
        color_names = {
            "#00FF00": "Grün",
            "#FF0000": "Rot",
            "#0000FF": "Blau", 
            "#FFFF00": "Gelb",
            "#FF00FF": "Lila",
            "#00FFFF": "Cyan",
            "rainbow": "Regenbogen"
        }
        return color_names.get(cls.CURRENT_COLOR, "Regenbogen")
    
    @classmethod
    def _get_pattern_display_name(cls):
        """Gibt benutzerfreundlichen Namen für Pattern zurück"""
        if cls.VISUALIZATION_MODE == "audio":
            return "Spektrum"
        elif cls.VISUALIZATION_MODE == "static":
            return "Statisch"
        else:
            return "Standard"


# ========================================
# AUTOMATISCHES LADEN BEIM IMPORT
# ========================================
# Konfiguration automatisch beim Import laden
Config.load_from_json()

# Validierung
if Config.LEFT_STRIP_LEDS <= 0 or Config.RIGHT_STRIP_LEDS <= 0:
    raise ValueError("LED-Anzahl muss größer als 0 sein!")

if Config.LEFT_STRIP_PIN == Config.RIGHT_STRIP_PIN:
    raise ValueError("Beide Strips können nicht den gleichen Pin verwenden!")

print(f"🚀 Config geladen: {Config.LEFT_STRIP_LEDS}L + {Config.RIGHT_STRIP_LEDS}R LEDs")