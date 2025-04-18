import time
import random
from rpi_ws281x import Color
from config.config import Config
from led_controllers.base_controller import BaseLEDController

class AudioVisualizer(BaseLEDController):
    def __init__(self):
        """Initialisiert den Audio-Visualizer"""
        super().__init__()
        
        # Interne Zustände für Simulation
        self._animation_step = 0
        self._last_update_time = time.time()
    
    def update(self):
        """
        Aktualisiert die LED-Anzeige basierend auf dem in der Config definierten Muster.
        Diese Methode wird regelmäßig vom LED-Manager aufgerufen.
        
        Da wir den Audio-Visualizer später implementieren werden, zeigt diese Version
        nur eine einfache Simulation an.
        """
        # Bestimme das aktuelle Muster aus der Config
        pattern = Config.AUDIO_PATTERN
        
        # Aktualisiere Animation basierend auf dem Muster
        if pattern == 'audio_pattern_01':
            self._simulate_spectrum()
        elif pattern == 'audio_pattern_02':
            self._simulate_equalizer()
        elif pattern == 'audio_pattern_03':
            self._simulate_beat()
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
    
    # Simulierte Audio-Visualisierungen (Platzhalter)
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
    
    def _simulate_spectrum(self):
        """
        Simuliert ein Audio-Spektrum ohne tatsächliche Audiodaten.
        """
        # Aktualisiere Animation
        self._animation_step = (self._animation_step + 1) % 100
        
        # Simulierte "Spektrum"-Höhe basierend auf der Animation
        center = Config.LED_PER_STRIP // 2
        
        for i in range(Config.LED_PER_STRIP):
            # Berechne Abstand vom Zentrum
            distance = abs(i - center)
            
            # Simuliere einen pulsierenden Effekt
            intensity = max(0, 255 - distance * 30 - self._animation_step)
            
            # Farbe basierend auf Position
            hue = i / float(Config.LED_PER_STRIP)
            color = self._get_rainbow_color(hue, intensity)
            
            self.strip_one.setPixelColor(i, color)
            self.strip_two.setPixelColor(i, color)
        
        self.strip_one.show()
        self.strip_two.show()
        
        # Kleine Pause für Animation
        time.sleep(0.02)
    
    def _simulate_equalizer(self):
        """
        Simuliert einen Equalizer ohne tatsächliche Audiodaten.
        """
        # Aktualisiere Animation
        self._animation_step = (self._animation_step + 1) % 20
        
        # Teile den LED-Streifen in Equalizer-Bänder auf
        num_bands = 5
        leds_per_band = Config.LED_PER_STRIP // num_bands
        
        for band in range(num_bands):
            # Simulierte Höhe für jedes Band
            height = random.randint(1, leds_per_band)
            
            # Färbe die LEDs in diesem Band
            for i in range(leds_per_band):
                led_index = band * leds_per_band + i
                
                if led_index < Config.LED_PER_STRIP:
                    if i < height:
                        # Farbe basierend auf Band-Position
                        hue = band / float(num_bands)
                        color = self._get_rainbow_color(hue, 255)
                    else:
                        color = Color(0, 0, 0)  # Aus
                    
                    self.strip_one.setPixelColor(led_index, color)
                    self.strip_two.setPixelColor(led_index, color)
        
        self.strip_one.show()
        self.strip_two.show()
        
        # Kleine Pause für Animation
        time.sleep(0.1)
    
    def _simulate_beat(self):
        """
        Simuliert einen Beat-Reaktions-Effekt ohne tatsächliche Audiodaten.
        """
        # Aktualisiere Animation
        self._animation_step = (self._animation_step + 1) % 30
        
        # Simuliere einen Beat alle 15 Schritte
        if self._animation_step == 0 or self._animation_step == 15:
            # Beat-Effekt: Alle LEDs leuchten hell auf
            color = self._get_color_from_config()
            
            for i in range(Config.LED_PER_STRIP):
                self.strip_one.setPixelColor(i, color)
                self.strip_two.setPixelColor(i, color)
        else:
            # Zwischen Beats: Dimme alle LEDs
            intensity = max(0, 100 - abs(self._animation_step - 15) * 15)
            
            for i in range(Config.LED_PER_STRIP):
                r, g, b = self._scale_color(self._get_color_from_config(), intensity / 100.0)
                color = Color(r, g, b)
                
                self.strip_one.setPixelColor(i, color)
                self.strip_two.setPixelColor(i, color)
        
        self.strip_one.show()
        self.strip_two.show()
        
        # Kleine Pause für Animation
        time.sleep(0.03)
    
    # Hilfsmethoden für Farben
    def _get_rainbow_color(self, hue, intensity=255):
        """
        Gibt eine Regenbogenfarbe basierend auf dem Farbton zurück.
        
        :param hue: Farbton (0-1)
        :param intensity: Helligkeit (0-255)
        :return: Color-Objekt
        """
        # Konvertiere Farbton zu RGB
        r, g, b = 0, 0, 0
        
        if hue < 1/6:
            r = 255
            g = int(hue * 6 * 255)
        elif hue < 2/6:
            r = int((2/6 - hue) * 6 * 255)
            g = 255
        elif hue < 3/6:
            g = 255
            b = int((hue - 2/6) * 6 * 255)
        elif hue < 4/6:
            g = int((4/6 - hue) * 6 * 255)
            b = 255
        elif hue < 5/6:
            r = int((hue - 4/6) * 6 * 255)
            b = 255
        else:
            r = 255
            b = int((1 - hue) * 6 * 255)
        
        # Skaliere basierend auf Intensität
        r = int(r * intensity / 255)
        g = int(g * intensity / 255)
        b = int(b * intensity / 255)
        
        return Color(r, g, b)
    
    def _scale_color(self, color, factor):
        """
        Skaliert eine Farbe mit einem Faktor.
        
        :param color: Color-Objekt
        :param factor: Skalierungsfaktor (0-1)
        :return: (r, g, b)-Tupel
        """
        r = (color >> 16) & 0xFF
        g = (color >> 8) & 0xFF
        b = color & 0xFF
        
        r = int(r * factor)
        g = int(g * factor)
        b = int(b * factor)
        
        return r, g, b