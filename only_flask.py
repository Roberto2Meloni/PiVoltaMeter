from flask import Flask, render_template, request, jsonify
import only_led
import threading

app = Flask(__name__)

@app.route('/')
def index():
    """Startseite des Webservers"""
    return render_template('index.html')

@app.route('/run_all')
def run_all():
    """Führt alle LED-Sequenzen aus"""
    only_led.start_all_start_phase()
    return jsonify({"status": "success", "message": "Alle Sequenzen ausgeführt"})

@app.route('/sequence_one')
def sequence_one():
    """Führt Sequenz 1 aus"""
    only_led.start_phase_one()
    return jsonify({"status": "success", "message": "Sequenz 1 ausgeführt"})

@app.route('/sequence_two')
def sequence_two():
    """Führt Sequenz 2 aus"""
    only_led.start_phase_two()
    return jsonify({"status": "success", "message": "Sequenz 2 ausgeführt"})

@app.route('/sequence_three')
def sequence_three():
    """Führt Sequenz 3 aus"""
    only_led.start_phase_three()
    return jsonify({"status": "success", "message": "Sequenz 3 ausgeführt"})

@app.route('/pulse_leds', methods=['POST'])
def pulse_leds():
    """LEDs in der angegebenen Farbe pulsieren lassen"""
    data = request.get_json()
    color = data.get('color', '#3498db')  # Standardfarbe ist Blau
    cycles = int(data.get('cycles', 3))   # Standardmäßig 3 Zyklen
    
    only_led.pulsing_all_led(color, cycles)
    
    return jsonify({
        "status": "success", 
        "message": f"LEDs haben in Farbe {color} für {cycles} Zyklen pulsiert"
    })

@app.route('/set_color', methods=['POST'])
def set_color():
    """Setzt alle LEDs auf eine bestimmte Farbe"""
    data = request.get_json()
    color = data.get('color', '#3498db')  # Standardfarbe ist Blau
    
    # Hexwert in RGB-Komponenten umwandeln
    color_hex = color.lstrip('#')
    r = int(color_hex[0:2], 16)
    g = int(color_hex[2:4], 16)
    b = int(color_hex[4:6], 16)
    
    # Alle LEDs auf die gewählte Farbe setzen
    for i in range(only_led.LED_PER_STRIP):
        only_led.strip_one.setPixelColor(i, only_led.Color(r, g, b))
        only_led.strip_two.setPixelColor(i, only_led.Color(r, g, b))
    only_led.strip_one.show()
    only_led.strip_two.show()
    
    return jsonify({
        "status": "success", 
        "message": f"LEDs auf Farbe {color} gesetzt"
    })

@app.route('/turn_off', methods=['POST'])
def turn_off():
    """Schaltet alle LEDs aus"""
    for i in range(only_led.LED_PER_STRIP):
        only_led.strip_one.setPixelColor(i, only_led.Color(0, 0, 0))
        only_led.strip_two.setPixelColor(i, only_led.Color(0, 0, 0))
    only_led.strip_one.show()
    only_led.strip_two.show()
    
    return jsonify({
        "status": "success", 
        "message": "Alle LEDs ausgeschaltet"
    })

def start_flask_server():
    """Startet den Flask-Webserver mit Animations-Feedback"""
    print("Starte Flask-Webserver...")
    
    # Zeige Animation für Webserver-Start
    only_led.animation_webserver_starting(iterations=1)
    
    try:
        # Bereite die App vor
        app.debug = False  # Debug-Modus muss aus sein
        
        # Zeige Animation für Webserver-bereit
        only_led.animation_webserver_ready()
        
        # Starte den Server im Hauptthread
        app.run(host='0.0.0.0', port=5000, threaded=True)
        
    except Exception as e:
        print(f"Fehler beim Starten des Webservers: {e}")
        # Zeige Fehler-Animation
        only_led.animation_webserver_error(loop=True)