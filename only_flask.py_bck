from flask import Flask, render_template, request, jsonify
import only_led
from rpi_ws281x import Color
# Im Flask-Server oder beim Start deiner Anwendung


# Importieren Sie die Konfiguration
from config.config import Config

# Globale Variablen definieren
current_visualizer = None
visualization_thread = None

app = Flask(__name__)

# Globale Variable für LED-Manager
led_manager = None


@app.route('/')
def index():
    """Startseite des Webservers mit vorgeladener Konfiguration"""
    # Hole die aktuelle Konfiguration
    config_json = Config.to_json()
    
    # Übergebe die Konfiguration als Variable an das Template
    return render_template('index.html', config=config_json)


@app.route('/set_visualization_mode', methods=['POST'])
def set_visualization_mode():
    data = request.get_json()
    current_mode = Config.VISUALIZATION_MODE
    new_mode = data.get('mode', 'audio') # sollte kein 'mode' gesendet werden, verwende 'audio' als Standartwert

    print(f"Aktueller modus: {current_mode}")
    print(f"Empfangener modus: {new_mode}")

    try:
        # Validieren und umstellen des Modus
        if new_mode in ['audio', 'static', 'off']:
            Config.set_visualization_mode(new_mode)

            # LED-Manager über Änderung informieren
            if led_manager:
                led_manager.handle_config_change()
            
            # Vollständige Konfiguration zurückgeben
            return jsonify({
                "status": "success", 
                "message": f"Visualisierungs Modus umgestellt auf {new_mode}",
                "config": Config.to_json()
            })
        else:
            return jsonify({
                "status": "error", 
                "message": f"Ungültiger Modus: {new_mode}. Erlaubte Modi: audio, pattern, off"
            }), 400
    except ValueError as e:
        return jsonify({
            "status": "error", 
            "message": str(e)
        }), 400

@app.route('/set_pattern_per_mode', methods=['POST'])
def set_pattern_per_mode():
    data = request.get_json()
    new_pattern = data.get('pattern')
    current_mode = Config.VISUALIZATION_MODE
    
    # Ermittle aktuelles Muster für Debugging
    if current_mode == 'audio':
        current_pattern = Config.AUDIO_PATTERN
    elif current_mode == 'static':
        current_pattern = Config.STATIC_PATTERN
    else:
        current_pattern = "off"

    # Debug-Ausgaben
    print(f"Aktuelles Muster: {current_pattern}")
    print(f"Empfangenes Muster: {new_pattern}")

    # Muster-Update versuchen
    try:
        if new_pattern:
            Config.set_pattern_per_mode(new_pattern)
            
            # Hole das aktualisierte Muster zur Bestätigung
            if current_mode == 'audio':
                updated_pattern = Config.AUDIO_PATTERN
                pattern_name = new_pattern.replace('audio_pattern_', 'Audio-Muster ')
            elif current_mode == 'static':
                updated_pattern = Config.STATIC_PATTERN
                pattern_name = new_pattern.replace('static_pattern_', 'Statisches Muster ')
            else:
                updated_pattern = "off"
                pattern_name = "Aus"

            # LED-Manager über Änderung informieren
            if led_manager:
                led_manager.handle_config_change()
                
            # Erfolgsantwort mit vollständiger Konfiguration
            print("Wechsel Muster Erfolg")
            return jsonify({
                "status": "success",
                "message": f"Muster erfolgreich auf {pattern_name} umgestellt",
                "config": Config.to_json()
            })
        else:
            print("Wechsel Muster KEIN Erfolg")
            return jsonify({
                "status": "error",
                "message": "Kein Muster angegeben"
            }), 400
    except ValueError as e:
        print(f"Fehler beim Musterwechsel {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

@app.route('/set_color', methods=['POST'])
def set_color():
    data = request.get_json()
    color = data.get('color', 'rainbow')
    
    try:
        # Hier die Farbe im Config-Objekt speichern
        Config.LED_COLOR = color
        # LED-Manager über Änderung informieren
        if led_manager:
            led_manager.handle_config_change()

        
        # Vollständige Konfiguration zurückgeben
        return jsonify({
            "status": "success",
            "message": f"Farbe auf {color} umgestellt",
            "config": Config.to_json()
        })
    except ValueError as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

# Neue Route zum direkten Abrufen der aktuellen Konfiguration
@app.route('/get_current_config', methods=['GET'])
def get_current_config():
    """
    Gibt die aktuelle Konfiguration als JSON zurück.
    Dies ist nützlich für die Initialisierung der Weboberfläche.
    """
    return jsonify({
        "status": "success",
        "config": Config.to_json()
    })


# Richtige Version
def start_flask_server(host='0.0.0.0', port=5000, led_manager_instance=None):
    """Startet den Flask-Server"""
    global led_manager
    led_manager = led_manager_instance
    app.run(host=host, port=port)