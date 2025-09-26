# LED-optimierte Konfiguration für PiVoltMeter
# Datum: 24.09.2025
# Version: 2.1 - Mit optimierten LED-Farben

import json
import os
import socket
from datetime import datetime
from pathlib import Path

class Config:
    """Zentrale Konfiguration mit LED-optimierten Farben"""
    
    # Pfad zur Konfigurations-JSON
    CONFIG_FILE = Path(__file__).parent / "config.json"
    
    # ========================================
    # LED-OPTIMIERTE FARBEN (Ihre Auswahl)
    # ========================================
    COLOR_MAP = {
        'regenbogen': 'rainbow',      # Spezialfall für Regenbogen-Effekt
        'gruen': '#00FF00',           # Reines Grün - sehr hell auf LEDs
        'blau': '#0080FF',            # Helles Blau - gut sichtbar  
        'rot': '#FF0000',             # Reines Rot - maximale Helligkeit
        'lila': '#8000FF',            # Helles Lila - gute LED-Darstellung
        'gelb': '#FFFF00',            # Reines Gelb - sehr hell
    }
    
    # Alternative deutsche Namen (falls gewünscht)
    COLOR_ALIASES = {
        'rainbow': 'regenbogen',
        'green': 'gruen',
        'blue': 'blau', 
        'red': 'rot',
        'purple': 'lila',
        'yellow': 'gelb'
    }
    
    # Umgekehrtes Mapping für Hex -> Name
    HEX_TO_NAME = {
        'rainbow': 'regenbogen',
        '#00FF00': 'gruen',
        '#0080FF': 'blau',
        '#FF0000': 'rot', 
        '#8000FF': 'lila',
        '#FFFF00': 'gelb'
    }
    
    # ========================================
    # HARDWARE-SETTINGS
    # ========================================
    LEFT_STRIP_PIN = 18
    RIGHT_STRIP_PIN = 13
    LED_FREQ_HZ = 800000
    LED_DMA_LEFT = 10
    LED_DMA_RIGHT = 11
    LED_INVERT = False
    LED_CHANNEL_LEFT = 0
    LED_CHANNEL_RIGHT = 1
    AUDIO_RATE = 44100
    AUDIO_CHUNK = 1024
    
    # ========================================
    # PERSISTENTE WERTE
    # ========================================
    LEFT_STRIP_LEDS = 10
    RIGHT_STRIP_LEDS = 10
    VISUALIZATION_MODE = 'audio'
    AUDIO_CHANNELS = 1
    
    LED_BRIGHTNESS = 50
    CURRENT_COLOR = '#8000FF'   # Standard: Lila (wie in Ihrem Bild "AKTIV")
    CURRENT_PATTERN = 'regenbogen'
    
    AUDIO_SMOOTHING = 0.3
    AMPLITUDE_COLOR_MODE = 'gradient'  # 'gradient' oder 'fixed'
    
    # Pattern-Konfiguration
    STATIC_PATTERN = 'static_pattern_01'
    
    # ========================================
    # FARBMANAGEMENT-METHODEN
    # ========================================
    @classmethod
    def get_current_color_name(cls):
        """Gibt den deutschen Farbnamen der aktuellen Farbe zurück"""
        return cls.HEX_TO_NAME.get(cls.CURRENT_COLOR, 'lila')
    
    @classmethod
    def get_current_color_hex(cls):
        """Gibt den Hex-Wert der aktuellen Farbe zurück"""
        if cls.CURRENT_COLOR == 'rainbow':
            return 'rainbow'
        return cls.CURRENT_COLOR
    
    @classmethod
    def set_color_by_name(cls, color_name):
        """Setzt Farbe über deutschen Farbnamen"""
        color_name = color_name.lower()
        
        # Prüfe direkte deutsche Namen
        if color_name in cls.COLOR_MAP:
            cls.CURRENT_COLOR = cls.COLOR_MAP[color_name]
            cls.save_to_json()
            print(f"🎨 Farbe gesetzt: {color_name} ({cls.CURRENT_COLOR})")
            return True
        
        # Prüfe englische Aliase
        if color_name in cls.COLOR_ALIASES:
            german_name = cls.COLOR_ALIASES[color_name]
            cls.CURRENT_COLOR = cls.COLOR_MAP[german_name]
            cls.save_to_json()
            print(f"🎨 Farbe gesetzt: {german_name} ({cls.CURRENT_COLOR})")
            return True
        
        # Fehler
        available_colors = ', '.join(cls.COLOR_MAP.keys())
        raise ValueError(f"Unbekannte Farbe '{color_name}'. Verfügbar: {available_colors}")
    
    @classmethod
    def set_color_by_hex(cls, hex_color):
        """Setzt Farbe über Hex-Wert"""
        hex_color = hex_color.upper()
        
        if hex_color.startswith('#') and len(hex_color) == 7:
            cls.CURRENT_COLOR = hex_color
            cls.save_to_json()
            color_name = cls.HEX_TO_NAME.get(hex_color, 'custom')
            print(f"🎨 Farbe gesetzt: {color_name} ({hex_color})")
            return True
        else:
            raise ValueError(f"Farbe muss Format '#RRGGBB' haben, erhalten: {hex_color}")
    
    @classmethod
    def get_available_colors(cls):
        """Gibt alle verfügbaren deutschen Farbnamen zurück"""
        return list(cls.COLOR_MAP.keys())
    
    @classmethod
    def get_color_info(cls):
        """Gibt detaillierte Farbinformationen zurück"""
        return {
            'current_name': cls.get_current_color_name(),
            'current_hex': cls.get_current_color_hex(),
            'available_colors': cls.get_available_colors(),
            'color_map': cls.COLOR_MAP
        }
    
    # ========================================
    # AUDIO-FARBMETHODEN
    # ========================================
    @classmethod
    def get_audio_color_hex(cls):
        """Gibt die Farbe für Audio-Visualisierung zurück"""
        if cls.AMPLITUDE_COLOR_MODE == 'fixed':
            return cls.CURRENT_COLOR
        else:
            return 'gradient'  # Grün-zu-Rot Gradient
    
    @classmethod
    def get_audio_color_name(cls):
        """Gibt den Farbnamen für Audio-Visualisierung zurück"""
        if cls.AMPLITUDE_COLOR_MODE == 'fixed':
            return cls.get_current_color_name()
        else:
            return 'gradient'
    
    @classmethod
    def set_audio_color_mode(cls, mode):
        """Setzt Audio-Farbmodus: 'gradient' oder 'fixed'"""
        if mode in ['gradient', 'fixed']:
            cls.AMPLITUDE_COLOR_MODE = mode
            cls.save_to_json()
            print(f"🎵 Audio-Farbmodus: {mode}")
            if mode == 'fixed':
                print(f"🎵 Audio verwendet jetzt: {cls.get_current_color_name()}")
        else:
            raise ValueError("Modus muss 'gradient' oder 'fixed' sein")
    
    # ========================================
    # STATIC-PATTERN FARBMETHODEN
    # ========================================
    @classmethod
    def get_static_color_hex(cls):
        """Gibt die Farbe für statische Muster zurück"""
        return cls.CURRENT_COLOR
    
    @classmethod
    def get_static_color_name(cls):
        """Gibt den Farbnamen für statische Muster zurück"""
        return cls.get_current_color_name()
    
    @classmethod
    def is_rainbow_mode(cls):
        """Prüft ob Regenbogen-Modus aktiv ist"""
        return cls.CURRENT_COLOR == 'rainbow' or cls.get_current_color_name() == 'regenbogen'
    
    # ========================================
    # PATTERN-METHODEN
    # ========================================
    @classmethod
    def set_pattern(cls, pattern_name):
        """Setzt das statische Muster"""
        valid_patterns = [
            'static_pattern_01',  # Einfacher Puls
            'static_pattern_02',  # Ping-Pong
            'static_pattern_03',  # Dual-Puls
            'static_pattern_04'   # Matrix-Regen
        ]
        
        if pattern_name in valid_patterns:
            cls.STATIC_PATTERN = pattern_name
            cls.save_to_json()
            print(f"🎨 Muster gesetzt: {pattern_name}")
        else:
            raise ValueError(f"Ungültiges Muster: {pattern_name}")
    
    @classmethod
    def get_pattern_info(cls):
        """Gibt Muster-Informationen zurück"""
        pattern_names = {
            'static_pattern_01': 'Einfacher Puls',
            'static_pattern_02': 'Ping-Pong',
            'static_pattern_03': 'Dual-Puls', 
            'static_pattern_04': 'Matrix-Regen'
        }
        
        return {
            'current_pattern': cls.STATIC_PATTERN,
            'current_name': pattern_names.get(cls.STATIC_PATTERN, 'Unbekannt'),
            'available_patterns': pattern_names
        }
    
    # ========================================
    # JSON LADEN/SPEICHERN
    # ========================================
    @classmethod
    def load_from_json(cls):
        """Lädt Konfiguration aus JSON"""
        if not cls.CONFIG_FILE.exists():
            print("📄 Erstelle neue config.json...")
            cls.save_to_json()
            return
            
        try:
            with open(cls.CONFIG_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Lade Werte
            cls.LEFT_STRIP_LEDS = data.get('left_strip_leds', cls.LEFT_STRIP_LEDS)
            cls.RIGHT_STRIP_LEDS = data.get('right_strip_leds', cls.RIGHT_STRIP_LEDS)
            cls.VISUALIZATION_MODE = data.get('visualization_mode', cls.VISUALIZATION_MODE)
            cls.AUDIO_CHANNELS = data.get('audio_channels', cls.AUDIO_CHANNELS)
            
            cls.LED_BRIGHTNESS = data.get('led_brightness', cls.LED_BRIGHTNESS)
            cls.CURRENT_COLOR = data.get('current_color', cls.CURRENT_COLOR)
            cls.CURRENT_PATTERN = data.get('current_pattern', cls.CURRENT_PATTERN)
            
            cls.AUDIO_SMOOTHING = data.get('audio_smoothing', cls.AUDIO_SMOOTHING)
            cls.AMPLITUDE_COLOR_MODE = data.get('amplitude_color_mode', cls.AMPLITUDE_COLOR_MODE)
            cls.STATIC_PATTERN = data.get('static_pattern', cls.STATIC_PATTERN)
            
            # Validiere Farbe
            if cls.CURRENT_COLOR not in cls.HEX_TO_NAME and cls.CURRENT_COLOR != 'rainbow':
                print(f"⚠️ Unbekannte Farbe {cls.CURRENT_COLOR}, setze auf Lila")
                cls.CURRENT_COLOR = '#8000FF'
            
            color_name = cls.get_current_color_name()
            print(f"✅ Config geladen: {cls.LEFT_STRIP_LEDS}L + {cls.RIGHT_STRIP_LEDS}R LEDs, Farbe: {color_name}")
            
        except Exception as e:
            print(f"⚠️ Fehler beim Laden: {e}")
            print("📄 Verwende Standard-Werte...")
    
    @classmethod
    def save_to_json(cls):
        """Speichert Konfiguration in JSON"""
        try:
            cls.CONFIG_FILE.parent.mkdir(exist_ok=True)
            
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
                "static_pattern": cls.STATIC_PATTERN,
                
                # Zusätzliche Info für Debugging
                "_color_name": cls.get_current_color_name(),
                "_last_updated": datetime.now().isoformat()
            }
            
            with open(cls.CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print("💾 Konfiguration gespeichert")
            
        except Exception as e:
            print(f"❌ Fehler beim Speichern: {e}")
    
    # ========================================
    # ERWEITERTE SETTER
    # ========================================
    @classmethod
    def set_visualization_mode(cls, mode):
        """Ändert Visualisierungsmodus"""
        valid_modes = ['audio', 'pattern', 'off']
        if mode in valid_modes:
            cls.VISUALIZATION_MODE = mode
            cls.save_to_json()
            print(f"🎨 Modus: {mode}")
        else:
            raise ValueError(f"Modus muss einer von {valid_modes} sein!")
    
    @classmethod
    def set_brightness(cls, brightness):
        """Setzt LED-Helligkeit (0-255)"""
        if 0 <= brightness <= 255:
            cls.LED_BRIGHTNESS = brightness
            cls.save_to_json()
            print(f"💡 Helligkeit: {brightness}/255")
        else:
            raise ValueError("Helligkeit muss zwischen 0 und 255 sein!")
    
    # ========================================
    # INFO & DEBUG
    # ========================================
    @classmethod
    def print_config(cls):
        """Zeigt aktuelle Konfiguration"""
        print("=" * 50)
        print("🎛️ PiVoltMeter Konfiguration")
        print("=" * 50)
        print(f"📍 Linker Strip:  {cls.LEFT_STRIP_LEDS} LEDs an GPIO {cls.LEFT_STRIP_PIN}")
        print(f"📍 Rechter Strip: {cls.RIGHT_STRIP_LEDS} LEDs an GPIO {cls.RIGHT_STRIP_PIN}")
        print(f"💡 Helligkeit:    {cls.LED_BRIGHTNESS}/255")
        print(f"🎨 Modus:         {cls.VISUALIZATION_MODE}")
        print(f"🎨 Farbe:         {cls.get_current_color_name()} ({cls.CURRENT_COLOR})")
        print(f"🎵 Audio-Modus:   {cls.AMPLITUDE_COLOR_MODE}")
        
        if cls.VISUALIZATION_MODE == 'static':
            pattern_info = cls.get_pattern_info()
            print(f"🎭 Muster:        {pattern_info['current_name']}")
        
        print(f"📂 Config-Datei:  {cls.CONFIG_FILE}")
        print("=" * 50)
        
        # Zeige verfügbare Farben
        print("🎨 Verfügbare Farben:")
        for name, hex_val in cls.COLOR_MAP.items():
            active = "✓" if cls.get_current_color_name() == name else " "
            print(f"  {active} {name}: {hex_val}")
        print("=" * 50)
    
    @classmethod
    def to_json(cls):
        """Gibt aktuelle Konfiguration als Dictionary für Templates zurück"""
        try:
            return {
                "left_strip_leds": cls.LEFT_STRIP_LEDS,
                "right_strip_leds": cls.RIGHT_STRIP_LEDS,
                "visualization_mode": cls.VISUALIZATION_MODE,
                "audio_channels": cls.AUDIO_CHANNELS,
                "led_brightness": cls.LED_BRIGHTNESS,
                "current_color": cls.CURRENT_COLOR,
                "current_color_name": cls.get_current_color_name(),
                "current_pattern": cls.CURRENT_PATTERN,
                "audio_smoothing": float(cls.AUDIO_SMOOTHING),
                "amplitude_color_mode": cls.AMPLITUDE_COLOR_MODE,
                "static_pattern": cls.STATIC_PATTERN,
                
                # Farbinformationen für Frontend
                "color_info": cls.get_color_info(),
                "pattern_info": cls.get_pattern_info(),
                "is_rainbow": cls.is_rainbow_mode(),
                
                # Hardware-Info
                "hardware": {
                    "left_strip_pin": cls.LEFT_STRIP_PIN,
                    "right_strip_pin": cls.RIGHT_STRIP_PIN,
                    "max_leds": max(cls.LEFT_STRIP_LEDS, cls.RIGHT_STRIP_LEDS),
                    "total_leds": cls.LEFT_STRIP_LEDS + cls.RIGHT_STRIP_LEDS
                }
            }
        except Exception as e:
            print(f"⚠️ Fehler bei to_json(): {e}")
            return {
                "left_strip_leds": 10,
                "right_strip_leds": 10,
                "visualization_mode": "audio",
                "current_color": "#8000FF",
                "current_color_name": "lila",
                "led_brightness": 50
            }

# ========================================
# AUTOMATISCHES LADEN
# ========================================
Config.load_from_json()

# Validierung
if Config.LEFT_STRIP_LEDS <= 0 or Config.RIGHT_STRIP_LEDS <= 0:
    raise ValueError("LED-Anzahl muss größer als 0 sein!")

if Config.LEFT_STRIP_PIN == Config.RIGHT_STRIP_PIN:
    raise ValueError("Beide Strips können nicht den gleichen Pin verwenden!")

print(f"🚀 Config geladen: {Config.LEFT_STRIP_LEDS}L + {Config.RIGHT_STRIP_LEDS}R LEDs, Farbe: {Config.get_current_color_name()}")