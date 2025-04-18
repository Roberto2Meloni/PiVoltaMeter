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
            self._visualize_simple_pulsing()
        elif pattern == 'static_pattern_02':
            self._visualize_simple_pulsing()
        elif pattern == 'static_pattern_03':
            self._visualize_simple_pulsing()
        elif pattern == 'static_pattern_04':
            self._visualize_simple_pulsing()
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
        Schaltet alle LEDs aus - auch die außerhalb des normalen Bereichs
        """
        print("Schalte ALLE LEDs aus (erweiterte Version)")
        
        # Verwende einen höheren Wert, um sicherzustellen, dass alle LEDs erreicht werden
        max_leds = max(Config.LED_PER_STRIP, 20)  # Stelle sicher, dass mindestens 20 LEDs angesprochen werden
        
        # Alle LEDs auf Schwarz setzen
        for i in range(max_leds):
            self.strip_one.setPixelColor(i, Color(0, 0, 0))
            self.strip_two.setPixelColor(i, Color(0, 0, 0))
        
        # Strips aktualisieren
        self.strip_one.show()
        time.sleep(0.05)  # Etwas längere Pause
        self.strip_two.show()
        time.sleep(0.05)
        
        # Nochmals mit einem anderen Ansatz versuchen
        for i in range(max_leds-1, -1, -1):  # Rückwärts durchlaufen
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

    def _visualize_simple_pulsing(self):
        """
        Zeigt eine einfache, pulsierende Animation, die sich von links nach rechts bewegt.
        """
        # Falls noch nicht vorhanden, initialisiere die Position für die Animation
        if not hasattr(self, '_pulse_position'):
            self._pulse_position = 0
        
        # Alle LEDs zunächst ausschalten
        for i in range(Config.LED_PER_STRIP):
            self.strip_one.setPixelColor(i, Color(0, 0, 0))
            self.strip_two.setPixelColor(i, Color(0, 0, 0))
        
        # Bestimme die Position des Pulses
        pulse_width = 3  # Breite des Pulses in LEDs
        
        # Prüfe, ob Regenbogen-Modus aktiv ist
        is_rainbow = Config.LED_COLOR.lower() == 'rainbow'
        
        if not is_rainbow:
            # Normaler Farbmodus - hole die Farbe aus der Konfiguration
            color = self._get_color_from_config()
            base_r = (color >> 16) & 0xFF
            base_g = (color >> 8) & 0xFF
            base_b = color & 0xFF
        
        # Für jede LED in der Nähe des Pulses
        for i in range(Config.LED_PER_STRIP):
            # Berechne den Abstand zum Puls-Zentrum
            distance = abs(i - self._pulse_position)
            
            # Wenn die LED innerhalb der Pulsbreite liegt
            if distance < pulse_width:
                # Intensität nimmt mit Abstand vom Zentrum ab
                intensity = 1.0 - (distance / pulse_width)
                
                if is_rainbow:
                    # Im Regenbogen-Modus: Farbe basierend auf Position im Strip
                    hue = i / float(Config.LED_PER_STRIP)
                    if hue < 1/6:
                        r = 255
                        g = int(hue * 6 * 255)
                        b = 0
                    elif hue < 2/6:
                        r = int((2/6 - hue) * 6 * 255)
                        g = 255
                        b = 0
                    elif hue < 3/6:
                        r = 0
                        g = 255
                        b = int((hue - 2/6) * 6 * 255)
                    elif hue < 4/6:
                        r = 0
                        g = int((4/6 - hue) * 6 * 255)
                        b = 255
                    elif hue < 5/6:
                        r = int((hue - 4/6) * 6 * 255)
                        g = 0
                        b = 255
                    else:
                        r = 255
                        g = 0
                        b = int((1 - hue) * 6 * 255)
                    
                    # Skaliere mit der Intensität
                    r = int(r * intensity)
                    g = int(g * intensity)
                    b = int(b * intensity)
                else:
                    # Im normalen Farbmodus: Skaliere die Basisfarbe mit der Intensität
                    r = int(base_r * intensity)
                    g = int(base_g * intensity)
                    b = int(base_b * intensity)
                
                # Setze die Farbe für beide LED-Streifen
                self.strip_one.setPixelColor(i, Color(r, g, b))
                self.strip_two.setPixelColor(i, Color(r, g, b))
        
        # Aktualisiere die LED-Streifen
        self.strip_one.show()
        self.strip_two.show()
        
        # Bewege den Puls für die nächste Aktualisierung
        self._pulse_position = (self._pulse_position + 1) % Config.LED_PER_STRIP
        
        # Kleine Pause für gleichmäßige Animation
        time.sleep(0.1)

    
    def _visualize_fire(self):
        """
        Zeigt ein animiertes Feuer-Muster an.
        """
        # Speichere den Zustand für die Feuer-Simulation, falls er noch nicht existiert
        if not hasattr(self, '_fire_values'):
            self._fire_values = [0] * Config.LED_PER_STRIP
        
        # Aktualisiere die Feuer-Simulation
        # Beginne mit zufälligen Werten am unteren Ende
        self._fire_values[0] = min(255, max(0, self._fire_values[0] + random.randint(-40, 40)))
        self._fire_values[1] = min(255, max(0, self._fire_values[1] + random.randint(-40, 40)))
        
        # Berechne die Ausbreitung und das Abkühlen des Feuers
        for i in range(2, Config.LED_PER_STRIP):
            # Das Feuer kühlt ab, je weiter es nach oben steigt
            cooling_factor = 0.8
            # Die Farbe basiert auf den Werten der darunter liegenden LEDs
            avg_below = (self._fire_values[i-1] + self._fire_values[i-2]) / 2
            # Füge etwas Zufall hinzu
            random_factor = random.uniform(0.9, 1.1)
            
            # Neuer Wert für diese LED
            new_value = min(255, max(0, int(avg_below * cooling_factor * random_factor)))
            self._fire_values[i] = new_value
        
        # Zeige die Feuer-Animation auf den LEDs an
        for i in range(Config.LED_PER_STRIP):
            # Invertiere die Position, damit das Feuer von unten nach oben geht
            pos = Config.LED_PER_STRIP - 1 - i
            
            # Farbe basierend auf dem Feuerwert
            intensity = self._fire_values[i]
            
            # Feuerfarbe: Rot bis Gelb, je nach Intensität
            r = intensity
            g = int(intensity * 0.4)  # Weniger Grün für ein rötlicheres Feuer
            b = 0
            
            color = Color(r, g, b)
            
            # Setze die Farbe für beide LED-Streifen
            self.strip_one.setPixelColor(pos, color)
            self.strip_two.setPixelColor(pos, color)
        
        # Aktualisiere die LED-Streifen
        self.strip_one.show()
        self.strip_two.show()
        
        # Kleine Pause für gleichmäßige Animation
        time.sleep(0.05)
    
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