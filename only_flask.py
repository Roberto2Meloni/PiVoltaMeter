from flask import Flask, render_template, request, jsonify
import threading
import time

# Importiere die neuen Visualisierungsklassen
from config.config import Config
from led_controllers.audio_visualizer import AudioVisualizer
from led_controllers.pattern_visualizer import PatternVisualizer

app = Flask(__name__)

# Globale Visualisierungs-Instanz
current_visualizer = None
visualization_thread = None

@app.route('/')
def index():
    """Startseite des Webservers"""
    return render_template('index.html')

@app.route('/change_mode', methods=['POST'])
def change_visualization_mode():
    """
    Ändert den Visualisierungsmodus
    """
    global current_visualizer, visualization_thread
    
    # Stoppe aktuellen Visualisierungsmodus
    if current_visualizer:
        if hasattr(current_visualizer, 'stop_visualization'):
            current_visualizer.stop_visualization()
        
        # Warte auf Thread-Beendigung
        if visualization_thread and visualization_thread.is_alive():
            visualization_thread.join(timeout=2)
    
    # Hole Modus aus Anfrage
    data = request.get_json()
    mode = data.get('mode', Config.VISUALIZATION_MODE)
    
    # Aktualisiere Konfiguration
    Config.set_visualization_mode(mode)
    
    # Wähle passenden Visualisierer
    if mode == 'audio':
        current_visualizer = AudioVisualizer()
        visualization_thread = threading.Thread(target=current_visualizer.start_visualization)
    elif mode == 'pattern':
        current_visualizer = PatternVisualizer()
        # Optional: Spezifisches Muster übergeben
        pattern = data.get('pattern', Config.DEFAULT_PATTERN)
        visualization_thread = threading.Thread(
            target=current_visualizer.start_pattern, 
            kwargs={'pattern_name': pattern}
        )
    else:
        # Fallback: Alle LEDs ausschalten
        current_visualizer = BaseLEDController()
        current_visualizer.clear_leds()
        return jsonify({
            "status": "success", 
            "message": f"Modus auf {mode} geändert"
        })
    
    # Starte neuen Thread
    visualization_thread.daemon = True
    visualization_thread.start()
    
    return jsonify({
        "status": "success", 
        "message": f"Modus auf {mode} geändert"
    })

@app.route('/set_pattern', methods=['POST'])
def set_pattern():
    """
    Setzt ein bestimmtes LED-Muster
    """
    global current_visualizer, visualization_thread
    
    # Stelle sicher, dass der aktuelle Modus 'pattern' ist
    if Config.VISUALIZATION_MODE != 'pattern':
        Config.set_visualization_mode('pattern')
    
    # Stoppe aktuellen Visualisierungsmodus
    if current_visualizer:
        if hasattr(current_visualizer, 'stop_visualization'):
            current_visualizer.stop_visualization()
        
        # Warte auf Thread-Beendigung
        if visualization_thread and visualization_thread.is_alive():
            visualization_thread.join(timeout=2)
    
    # Hole Mustername
    data = request.get_json()
    pattern = data.get('pattern', Config.DEFAULT_PATTERN)
    
    # Erstelle PatternVisualizer
    current_visualizer = PatternVisualizer()
    
    # Starte Muster in neuem Thread
    visualization_thread = threading.Thread(
        target=current_visualizer.start_pattern, 
        kwargs={'pattern_name': pattern}
    )
    visualization_thread.daemon = True
    visualization_thread.start()
    
    return jsonify({
        "status": "success", 
        "message": f"Muster {pattern} gestartet"
    })

# Restliche bestehende Routen wie run_all(), sequence_one() etc. bleiben unverändert

def start_flask_server():
    """Startet den Flask-Webserver mit Animations-Feedback"""
    print("Starte Flask-Webserver...")
    
    # Importiere LED-Animationen
    import only_led
    
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