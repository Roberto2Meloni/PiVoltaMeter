from flask import Flask,  render_template, request, jsonify
from rpi_ws281x import Color
import time
import random
import builtins
import sys
import os

# Füge das Parent-Verzeichnis zum Python-Path hinzu
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from config.config import Config

# Flask-App erstellen
app = Flask(__name__)

# ========================================
# HELPER-FUNKTIONEN
# ========================================

def get_led_strips():
    """Holt die LED-Streifen aus main.py"""
    try:
        return builtins.led_strips
    except AttributeError:
        raise RuntimeError("LED-Streifen nicht initialisiert! Starte main.py zuerst.")

def hex_to_color(hex_string):
    """Konvertiert Hex-String zu rpi_ws281x Color"""
    hex_string = hex_string.lstrip('#')
    r = int(hex_string[0:2], 16)
    g = int(hex_string[2:4], 16) 
    b = int(hex_string[4:6], 16)
    return Color(r, g, b)

def set_all_leds_color(color_hex):
    """Setzt alle LEDs auf eine Farbe (beide Strips)"""
    left_strip, right_strip = get_led_strips()
    color = hex_to_color(color_hex)
    
    # Beide Strips setzen
    for i in range(Config.LEFT_STRIP_LEDS):  # links
        left_strip.setPixelColor(i, color)
    for i in range(Config.RIGHT_STRIP_LEDS):  # rechts
        right_strip.setPixelColor(i, color)
    
    left_strip.show()
    right_strip.show()
    



def clear_all_leds():
    """Schaltet alle LEDs aus"""
    left_strip, right_strip = get_led_strips()
    
    for i in range(Config.LED_PER_STRIP):
        left_strip.setPixelColor(i, Color(0, 0, 0))
        right_strip.setPixelColor(i, Color(0, 0, 0))
    
    left_strip.show()
    right_strip.show()

def random_color():
    """Generiert zufällige Farbe"""
    return Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# ========================================
# ANIMATIONS
# ========================================

def animation_sequence_one():
    """Start-Sequenz 1: LEDs nacheinander einschalten"""
    left_strip, right_strip = get_led_strips()
    clear_all_leds()
    
    for i in range(Config.LED_PER_STRIP):
        left_strip.setPixelColor(i, random_color())
        right_strip.setPixelColor(i, random_color())
        left_strip.show()
        right_strip.show()
        time.sleep(0.1)
    
    time.sleep(0.5)
    clear_all_leds()

def animation_pulse_leds(color_hex, cycles=3):
    """Pulsier-Animation"""
    left_strip, right_strip = get_led_strips()
    
    # Hex zu RGB
    color_hex = color_hex.lstrip('#')
    r_base = int(color_hex[0:2], 16)
    g_base = int(color_hex[2:4], 16)
    b_base = int(color_hex[4:6], 16)
    
    for cycle in range(cycles):
        # Aufhellen
        for brightness in range(0, 101, 5):
            factor = brightness / 100.0
            color = Color(int(r_base * factor), int(g_base * factor), int(b_base * factor))
            
            for i in range(Config.LED_PER_STRIP):
                left_strip.setPixelColor(i, color)
                right_strip.setPixelColor(i, color)
            
            left_strip.show()
            right_strip.show()
            time.sleep(0.02)
        
        # Abdunkeln
        for brightness in range(100, -1, -5):
            factor = brightness / 100.0
            color = Color(int(r_base * factor), int(g_base * factor), int(b_base * factor))
            
            for i in range(Config.LED_PER_STRIP):
                left_strip.setPixelColor(i, color)
                right_strip.setPixelColor(i, color)
            
            left_strip.show()
            right_strip.show()
            time.sleep(0.02)
    
    clear_all_leds()


# Hier sind die Routen

@app.route('/')
def index():
    """Startseite des Webservers mit vorgeladener Konfiguration"""
    # Hole die aktuelle Konfiguration
    config_json = Config.to_json()
    
    # Übergebe die Konfiguration als Variable an das Template
    return render_template('index.html', config=config_json)


@app.route('/set_color', methods=['POST'])
def set_color():
    """API: LEDs auf Farbe setzen"""
    try:
        print("--------------Farb Weschel empfangen-----------")
        data = request.get_json()
        color = data.get('hex_code',)
        print(f"Farbe = {color}")
        print(20 * "----")
        print(data)
        print(20 * "----")
        
        # Farbe setzen und in Config speichern
        set_all_leds_color(color)
        Config.set_current_color(color)
        Config.set_visualization_mode('static')
        
        return jsonify({
            "status": "success", 
            "message": f"LEDs auf {color} gesetzt"
        })
    except Exception as e:
        print(f"Fehle beim Farbwechsel {e}")
        return jsonify({"status": "error", "message": f"Fehler: {str(e)}"}), 500

@app.route('/set_amplitude_color', methods=['POST'])
def set_amplitude_color():
    """API: Audio-Amplituden-Farbe setzen"""
    try:
        data = request.get_json()
        color = data.get('color', '#00FF00')
        
        # Farbe in Config speichern
        Config.set_amplitude_color(color)
        
        return jsonify({
            "status": "success", 
            "message": f"Audio-Farbe auf {color} gesetzt"
        })
    except Exception as e:
        return jsonify({"status": "error", "message": f"Fehler: {str(e)}"}), 500

@app.route('/pulse_leds', methods=['POST'])
def pulse_leds():
    """API: LED-Pulsieren"""
    try:
        data = request.get_json()
        color = data.get('color', '#00FF00')
        cycles = int(data.get('cycles', 3))
        
        animation_pulse_leds(color, cycles)
        
        return jsonify({
            "status": "success", 
            "message": f"LEDs pulsiert in {color} für {cycles} Zyklen"
        })
    except Exception as e:
        return jsonify({"status": "error", "message": f"Fehler: {str(e)}"}), 500

@app.route('/turn_off', methods=['POST'])
def turn_off():
    """API: Alle LEDs ausschalten"""
    try:
        clear_all_leds()
        return jsonify({"status": "success", "message": "Alle LEDs ausgeschaltet"})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Fehler: {str(e)}"}), 500

@app.route('/set_visualization_mode', methods=['POST'])
def set_visualization_mode():
    """API: Visualisierungsmodus setzen (für HTML-Template)"""
    try:
        data = request.get_json()
        mode = data.get('mode', 'audio')
        
        Config.set_visualization_mode(mode)
        
        return jsonify({
            "status": "success", 
            "message": f"Visualisierungsmodus auf {mode} gesetzt"
        })
    except Exception as e:
        return jsonify({"status": "error", "message": f"Fehler: {str(e)}"}), 500

@app.route('/set_pattern_per_mode', methods=['POST'])
def set_pattern_per_mode():
    """API: Pattern/Muster für bestimmten Modus setzen"""
    try:
        data = request.get_json()
        pattern = data.get('pattern', 'rainbow')
        mode = data.get('mode', 'audio')
        
        # Pattern in Config speichern
        Config.CURRENT_PATTERN = pattern
        
        # Falls nötig, Visualisierungsmodus auch ändern
        if mode:
            Config.set_visualization_mode(mode)
        
        # Config speichern
        Config.save_to_json()
        
        return jsonify({
            "status": "success", 
            "message": f"Pattern {pattern} für Modus {mode} gesetzt"
        })
    except Exception as e:
        return jsonify({"status": "error", "message": f"Fehler: {str(e)}"}), 500
