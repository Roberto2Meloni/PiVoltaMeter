from flask import Flask,  render_template, request, jsonify
from .app import app, set_all_leds_color, animation_pulse_leds, clear_all_leds
from config.config import Config

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
        print("--------------Farb Wechsel empfangen-----------")
        data = request.get_json()
        color = data.get('hex_code')
        print(f"Farbe = {color}")
        print(20 * "----")
        print(data)
        print(20 * "----")
        
        # LÖSUNG 1: Direkte Zuweisung (einfach)
        # Config.CURRENT_COLOR = color
        
        # LÖSUNG 2: Verwende die Config-Methode (empfohlen)
        Config.set_color_by_hex(color)
        
        # LEDs setzen
        set_all_leds_color(color)
        
        return jsonify({
            "status": "success", 
            "message": f"LEDs auf {color} gesetzt"
        })
    except Exception as e:
        print(f"Fehler beim Farbwechsel: {e}")
        import traceback
        traceback.print_exc()  # Zeigt vollständigen Fehler-Stack
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
        print(f"Der neue Modusl lautet: {mode}")
        
        Config.VISUALIZATION_MODE = mode


        if mode == "off":
            print("Schalt LED aus, da mode off ist")
            clear_all_leds()
        
        if mode =="pattern":
            print("Weschsle wieder auf Museter mit Farben")
            set_all_leds_color(Config.CURRENT_COLOR)
        
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
