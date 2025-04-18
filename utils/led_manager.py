import threading
import time
from config.config import Config
from led_controllers.audio_visualizer import AudioVisualizer
from led_controllers.pattern_visualizer import PatternVisualizer

class LEDManager:
    def __init__(self):
        self.audio_visualizer = AudioVisualizer()
        self.pattern_visualizer = PatternVisualizer()
        self.current_thread = None
        self.stop_event = threading.Event()
        self.current_mode = None
    
    def start_visualization(self):
        # Stoppe laufende Visualisierung
        self.stop_visualization()
        
        # Starte neue Visualisierung basierend auf Config
        mode = Config.VISUALIZATION_MODE
        self.current_mode = mode
        
        if mode == 'off':
            self.turn_off_leds()
            return
        
        # Thread für entsprechenden Modus starten
        self.stop_event.clear()
        
        if mode == 'audio':
            self.current_thread = threading.Thread(target=self._run_audio_visualization)
        elif mode == 'static':
            self.current_thread = threading.Thread(target=self._run_pattern_visualization)
        
        self.current_thread.daemon = True
        self.current_thread.start()
    
    def _run_audio_visualization(self):
        # Audio-Visualisierung im Thread ausführen
        while not self.stop_event.is_set():
            self.audio_visualizer.update()
            time.sleep(0.01)
    
    def _run_pattern_visualization(self):
        # Pattern-Visualisierung im Thread ausführen
        while not self.stop_event.is_set():
            self.pattern_visualizer.update()
            time.sleep(0.01)
    
    def stop_visualization(self):
        if self.current_thread and self.current_thread.is_alive():
            self.stop_event.set()
            self.current_thread.join(timeout=2.0)
            self.current_thread = None
    
    def turn_off_leds(self):
        # LEDs ausschalten
        self.pattern_visualizer.clear_leds()
    
    def handle_config_change(self):
        """Reagiert auf Konfigurationsänderungen"""
        # Übergangsanimation abspielen
        self.pattern_visualizer.play_transition_animation()
        
        if self.current_mode != Config.VISUALIZATION_MODE:
            # Modus hat sich geändert, Visualisierung neu starten
            self.start_visualization()