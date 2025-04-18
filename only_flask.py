from flask import Flask, render_template, request, jsonify
import only_led
from rpi_ws281x import Color

# Importieren Sie die Konfiguration
from config.config import Config

# Globale Variablen definieren
current_visualizer = None
visualization_thread = None

app = Flask(__name__)



@app.route('/')
def index():
    """Startseite des Webservers"""
    return render_template('index.html')

# @app.route('/sequence_one')
# def sequence_one():
#     """Führt Sequenz 1 aus"""
#     only_led.start_phase_one()
#     return jsonify({"status": "success", "message": "Sequenz 1 ausgeführt"})

# @app.route('/sequence_two')
# def sequence_two():
#     """Führt Sequenz 2 aus"""
#     only_led.start_phase_two()
#     return jsonify({"status": "success", "message": "Sequenz 2 ausgeführt"})

# @app.route('/sequence_three')
# def sequence_three():
#     """Führt Sequenz 3 aus"""
#     only_led.start_phase_three()
#     return jsonify({"status": "success", "message": "Sequenz 3 ausgeführt"})

# @app.route('/run_all')
# def run_all():
#     """Führt alle LED-Sequenzen aus"""
#     only_led.start_all_start_phase()
#     return jsonify({"status": "success", "message": "Alle Sequenzen ausgeführt"})

@app.route('/set_visualization_mode', methods=['POST'])
def set_visualization_mode():
    data = request.get_json()
    current_mode = Config.VISUALIZATION_MODE
    new_mode = data.get('mode', 'audio')
    
    # debug
    print(f"Aktueller modus: {current_mode}")
    print(f"Empfangener modus: {new_mode}")

    # Validieren und umstellen des Modus
    if new_mode in ['audio', 'pattern', 'off']:
        Config.set_visualization_mode(new_mode)
        
        return jsonify({
            "status": "success", 
            "message": f"Visualisierungs Modus umgestellt auf {new_mode}",
            "config": {
                "visualization_mode": new_mode,
                "amplitude_color": Config.FIXED_AMPLITUDE_COLOR,
                "led_brightness": Config.LED_BRIGHTNESS
                # Fügen Sie hier weitere Config-Werte hinzu, die Sie benötigen
            }
        })
    else:
        return jsonify({
            "status": "error", 
            "message": f"Ungültiger Modus: {new_mode}. Erlaubte Modi: audio, pattern, off"
        }), 400


@app.route('/set_color', methods=['POST'])
def set_color():
    """Setzt alle LEDs auf eine bestimmte Farbe"""
    global current_visualizer, visualization_thread
    
    try:
        # Beende aktuelle Visualisierung, falls vorhanden
        if current_visualizer:
            if hasattr(current_visualizer, 'stop_visualization'):
                current_visualizer.stop_visualization()
            
            current_visualizer = None
        
        if visualization_thread and visualization_thread.is_alive():
            visualization_thread.join(timeout=2)
        
        # Setze Modus auf Statisch
        Config.set_visualization_mode('static')
        
        # Hole Farbwert aus JSON-Anfrage
        data = request.get_json()
        color = data.get('color', '#3498db')  # Standardfarbe ist Blau
        
        # Hexwert in RGB-Komponenten umwandeln
        color_hex = color.lstrip('#')
        r = int(color_hex[0:2], 16)
        g = int(color_hex[2:4], 16)
        b = int(color_hex[4:6], 16)
        
        # Alle LEDs auf die gewählte Farbe setzen
        for i in range(only_led.LED_PER_STRIP):
            only_led.strip_one.setPixelColor(i, Color(r, g, b))
            only_led.strip_two.setPixelColor(i, Color(r, g, b))
        
        only_led.strip_one.show()
        only_led.strip_two.show()
        
        return jsonify({
            "status": "success", 
            "message": f"LEDs auf Farbe {color} gesetzt"
        })
    
    except Exception as e:
        return jsonify({
            "status": "error", 
            "message": f"Fehler beim Setzen der Farbe: {str(e)}"
        }), 500

# @app.route('/turn_off', methods=['POST'])
# def turn_off():
#     """Schaltet alle LEDs aus"""
#     try:
#         for i in range(only_led.LED_PER_STRIP):
#             only_led.strip_one.setPixelColor(i, Color(0, 0, 0))
#             only_led.strip_two.setPixelColor(i, Color(0, 0, 0))
        
#         only_led.strip_one.show()
#         only_led.strip_two.show()
        
#         return jsonify({
#             "status": "success", 
#             "message": "Alle LEDs ausgeschaltet"
#         })
    
#     except Exception as e:
#         return jsonify({
#             "status": "error", 
#             "message": f"Fehler beim Ausschalten der LEDs: {str(e)}"
#         }), 500

# @app.route('/pulse_leds', methods=['POST'])
# def pulse_leds():
#     """Lässt LEDs in einer bestimmten Farbe pulsieren"""
#     try:
#         data = request.get_json()
#         color = data.get('color', '#3498db')  # Standardfarbe ist Blau
#         cycles = int(data.get('cycles', 3))   # Standardmäßig 3 Zyklen
        
#         # Rufe Pulsier-Funktion auf
#         only_led.pulsing_all_led(color, cycles)
        
#         return jsonify({
#             "status": "success", 
#             "message": f"LEDs haben in Farbe {color} für {cycles} Zyklen gepulst"
#         })
    
#     except Exception as e:
#         return jsonify({
#             "status": "error", 
#             "message": f"Fehler beim Pulsieren der LEDs: {str(e)}"
#         }), 500

def start_flask_server():
    """Startet den Flask-Webserver mit Animations-Feedback"""
    print("Starte Flask-Webserver...")
    
    # Zeige Animation für Webserver-Start
    only_led.animation_webserver_starting(iterations=1)
    
    try:
        # Bereite die App vor
        app.debug = False  # Debug-Modus muss aus sein
        
        # Zeige Animation für Webserver-bereit
        # only_led.animation_webserver_ready()
        
        # Starte den Server im Hauptthread
        app.run(host='0.0.0.0', port=5000, threaded=True)
        
    except Exception as e:
        print(f"Fehler beim Starten des Webservers: {e}")
        # Zeige Fehler-Animation
        only_led.animation_webserver_error(loop=True)


# @app.route('/set_amplitude_color', methods=['POST'])
# def set_amplitude_color():
#     """Setzt die Farbe für die Amplituden-Visualisierung"""
#     try:
#         data = request.get_json()
#         color = data.get('color', '#00FF00')  # Standardfarbe Grün
#         print(f"Wechsel Farbe für Amplitude auf auf {color} | Defualt 00FF00")
        
#         # Setze Farbe in Konfiguration
#         Config.set_amplitude_color(color)
        
#         return jsonify({
#             "status": "success", 
#             "message": f"Amplituden-Farbe auf {color} gesetzt"
#         })
    
#     except Exception as e:
#         return jsonify({
#             "status": "error", 
#             "message": f"Fehler beim Setzen der Amplituden-Farbe: {str(e)}"
#         }), 500