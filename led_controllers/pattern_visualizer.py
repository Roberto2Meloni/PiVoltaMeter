import colorsys
import time
import random
from .base_controller import BaseLEDController
from rpi_ws281x import Color
from config.config import Config

class PatternVisualizer(BaseLEDController):
    def __init__(self, config=None):
        """
        Initialisiert den Muster-Visualisierer
        
        :param config: Konfigurationsobjekt (optional)
        """
        super().__init__(config)
        self.config = config or Config
        self.current_pattern = self.config.DEFAULT_PATTERN

    def rainbow_cycle(self, wait_ms=20, iterations=5):
        """
        Regenbogen-Laufeffekt
        
        :param wait_ms: Wartezeit zwischen Farbschritten
        :param iterations: Anzahl der Durchläufe
        """
        for j in range(256 * iterations):
            for i in range(self.config.LED_PER_STRIP):
                # Berechne Farbton basierend auf der LED-Position
                color = self._wheel((int(i * 256 / self.config.LED_PER_STRIP) + j) & 255)
                
                # Setze Farbe für beide Streifen
                self.strip_one.setPixelColor(i, color)
                self.strip_two.setPixelColor(i, color)
            
            # Aktualisiere LED-Streifen
            self.strip_one.show()
            self.strip_two.show()
            
            # Kleine Verzögerung
            time.sleep(wait_ms / 1000.0)

    def random_color_chase(self, iterations=5):
        """
        Zufällige Farbverfolgung
        
        :param iterations: Anzahl der Durchläufe
        """
        for _ in range(iterations):
            # Zufällige Farbe für den aktuellen Durchlauf
            color = self._random_color()
            
            # LED für LED durchlaufen
            for i in range(self.config.LED_PER_STRIP):
                # Alle LEDs ausschalten
                self.clear_leds()
                
                # Aktuelle LED und benachbarte LEDs mit Farbe setzen
                for j in range(max(0, i-1), min(self.config.LED_PER_STRIP, i+2)):
                    self.strip_one.setPixelColor(j, color)
                    self.strip_two.setPixelColor(j, color)
                
                # Anzeigen und kurz warten
                self.strip_one.show()
                self.strip_two.show()
                time.sleep(0.1)

    def theater_chase(self, color=None, wait_ms=50, iterations=10):
        """
        Theater-Chase-Effekt
        
        :param color: Farbe für den Effekt (None für zufällige Farbe)
        :param wait_ms: Wartezeit zwischen Schritten
        :param iterations: Anzahl der Durchläufe
        """
        # Zufällige Farbe, wenn keine übergeben wurde
        if color is None:
            color = self._random_color()
        
        for _ in range(iterations):
            for q in range(3):
                for i in range(0, self.config.LED_PER_STRIP, 3):
                    # Nur jede dritte LED beleuchten
                    pos = i + q
                    if pos < self.config.LED_PER_STRIP:
                        self.strip_one.setPixelColor(pos, color)
                        self.strip_two.setPixelColor(pos, color)
                
                # Anzeigen
                self.strip_one.show()
                self.strip_two.show()
                time.sleep(wait_ms / 1000.0)
                
                # Alle LEDs ausschalten
                self.clear_leds()

    def start_pattern(self, pattern_name=None):
        """
        Startet ein bestimmtes LED-Muster
        
        :param pattern_name: Name des Musters (None für Standardmuster)
        """
        # Verwende Standardmuster, wenn keiner angegeben wurde
        pattern_name = pattern_name or self.config.DEFAULT_PATTERN
        
        # Wähle Muster basierend auf dem Namen
        patterns = {
            'rainbow': self.rainbow_cycle,
            'random_chase': self.random_color_chase,
            'theater_chase': self.theater_chase
        }
        
        # Muster ausführen
        if pattern_name in patterns:
            self.current_pattern = pattern_name
            patterns[pattern_name]()
        else:
            raise ValueError(f"Unbekanntes Muster: {pattern_name}")

    def _wheel(self, pos):
        """
        Generiert Regenbogenfarben für Wheel-Effekte
        
        :param pos: Position im Farbkreis (0-255)
        :return: Color-Objekt
        """
        # Farbkreis-Logik für Regenbogeneffekte
        if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Color(0, pos * 3, 255 - pos * 3)

    def _random_color(self):
        """
        Generiert eine zufällige Farbe
        
        :return: Color-Objekt
        """
        return Color(
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )