import colorsys
import time
import random
import math
from rpi_ws281x import Color
from config.config import Config
from led_controllers.base_controller import BaseLEDController

class PatternVisualizer(BaseLEDController):
    def __init__(self):
        """Initialisiert den Pattern-Visualizer"""
        super().__init__()
        
        # Interne Zustände für Animationen
        self._animation_step = 0
        self._last_update_time = time.time()
    
    def update(self):
        """
        Aktualisiert die LED-Anzeige basierend auf dem in der Config definierten Muster.
        Diese Methode wird regelmäßig vom LED-Manager aufgerufen.
        """
        # Bestimme das aktuelle Muster aus der Config
        pattern = Config.STATIC_PATTERN
        
        # Aktualisiere Animation basierend auf dem Muster
        if pattern == 'static_pattern_01':
            self._visualize_fire()
        elif pattern == 'static_pattern_02':
            self._visualize_water()
        elif pattern == 'static_pattern_03':
            self._visualize_rainbow()
        elif pattern == 'static_pattern_04':
            self._visualize_wave()
        else:
            # Fallback: Einfach die gewählte Farbe anzeigen
            self._visualize_solid_color()
    
    def configure_from_config(self):
        """
        Konfiguriert den Controller basierend auf der aktuellen Config.
        Diese Methode wird aufgerufen, wenn sich die Konfiguration ändert.
        """
        # Helligkeit setzen
        brightness = Config.LED_BRIGHTNESS
        self.strip_one.setBrightness(brightness)
        self.strip_two.setBrightness(brightness)
        
        # Andere Parameter aus der Config übernehmen
        self._animation_step = 0  # Animationen zurücksetzen
    
    def cleanup(self):
        """
        Bereinigt Ressourcen und bereitet den Controller auf das Beenden vor.
        """
        self.clear_all_leds()
    
    # Hilfsmethoden für die Musterimplementierung
    def _get_color_from_config(self):
        """
        Gibt die in der Config konfigurierte Farbe zurück.
        """
        color_name = Config.LED_COLOR.lower()
        
        if color_name == 'rainbow':
            # Regenbogenfarben werden in den spezifischen Visualisierungen behandelt
            return Color(255, 255, 255)  # Weiß als Fallback
        elif color_name == 'red':
            return Color(255, 0, 0)
        elif color_name == 'green':
            return Color(0, 255, 0)
        elif color_name == 'blue':
            return Color(0, 0, 255)
        elif color_name == 'purple':
            return Color(128, 0, 128)
        elif color_name == 'yellow':
            return Color(255, 255, 0)
        else:
            return Color(255, 255, 255)  # Weiß als Fallback
    
    def clear_all_leds(self):
        """
        Schaltet alle LEDs aus.
        """
        print("SChallte allte LED' saus")
        for i in range(Config.LED_PER_STRIP):
            self.strip_one.setPixelColor(i, Color(0, 0, 0))
            self.strip_two.setPixelColor(i, Color(0, 0, 0))
        
        self.strip_one.show()
        self.strip_two.show()
    
    # Musterimplementierungen - zunächst als Platzhalter
    def _visualize_solid_color(self):
        """
        Zeigt eine Volltonfarbe auf allen LEDs an.
        """
        color = self._get_color_from_config()
        
        for i in range(Config.LED_PER_STRIP):
            self.strip_one.setPixelColor(i, color)
            self.strip_two.setPixelColor(i, color)
        
        self.strip_one.show()
        self.strip_two.show()
    
    def _visualize_fire(self):
        """
        Zeigt ein Feuer-Muster an.
        """
        # Platzhalter - wird später implementiert
        pass
    
    def _visualize_water(self):
        """
        Zeigt ein Wasser-Muster an.
        """
        # Platzhalter - wird später implementiert
        pass
        
    def _visualize_rainbow(self):
        """
        Zeigt ein animiertes Regenbogen-Muster an.
        """
        # Erhöhe den Animationsschritt für die nächste Aktualisierung
        self._animation_step = (self._animation_step + 1) % 256
        
        for i in range(Config.LED_PER_STRIP):
            # Berechne Farbton basierend auf der LED-Position und dem aktuellen Animationsschritt
            position = (i * 256 // Config.LED_PER_STRIP + self._animation_step) % 256
            
            # Wandle Position in Regenbogenfarbe um
            if position < 85:
                color = Color(position * 3, 255 - position * 3, 0)
            elif position < 170:
                position -= 85
                color = Color(255 - position * 3, 0, position * 3)
            else:
                position -= 170
                color = Color(0, position * 3, 255 - position * 3)
            
            # Setze die Farbe für beide LED-Streifen
            self.strip_one.setPixelColor(i, color)
            self.strip_two.setPixelColor(i, color)
        
        # Aktualisiere die LED-Streifen
        self.strip_one.show()
        self.strip_two.show()
        
        # Kleine Pause für gleichmäßige Animation
        time.sleep(0.02)
    
    def _visualize_wave(self):
        """
        Zeigt ein Wellenmuster an.
        """
        # Platzhalter - wird später implementiert
        pass