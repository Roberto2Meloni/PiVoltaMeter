from rpi_ws281x import PixelStrip, Color
from config.config import Config
import time
import math


class BaseLEDController:
    def __init__(self, config=None):
        """
        Initialisiert den Basis-LED-Controller
        
        :param config: Konfigurationsobjekt (optional)
        """
        # Verwende Standardkonfiguration, wenn keine übergeben wird
        self.config = config or Config
        
        # Initialisiere LED-Streifen
        self.strip_one = PixelStrip(
            self.config.LED_PER_STRIP, 
            self.config.LED_PIN_ONE, 
            self.config.LED_FREQ_HZ, 
            self.config.LED_DMA_ONE, 
            self.config.LED_INVERT, 
            self.config.LED_BRIGHTNESS, 
            self.config.LED_CHANNEL_ONE
        )
        
        self.strip_two = PixelStrip(
            self.config.LED_PER_STRIP, 
            self.config.LED_PIN_TWO, 
            self.config.LED_FREQ_HZ, 
            self.config.LED_DMA_TWO, 
            self.config.LED_INVERT, 
            self.config.LED_BRIGHTNESS, 
            self.config.LED_CHANNEL_TWO
        )
        
        # Starte LED-Streifen
        self.strip_one.begin()
        self.strip_two.begin()
        
        # Alle LEDs initial ausschalten - verwende die tatsächliche Anzahl
        self.clear_leds_with_margin()

    def clear_leds_with_margin(self):
        """
        Schaltet alle LEDs aus und fügt einen Sicherheitspuffer hinzu,
        um sicherzustellen, dass alle physischen LEDs erreicht werden.
        """
        # Anzahl der LEDs plus Sicherheitspuffer (z.B. 50%)
        led_count_with_margin = int(self.config.LED_PER_STRIP * 1.5)
        
        for i in range(led_count_with_margin):
            self.strip_one.setPixelColor(i, Color(0, 0, 0))
            self.strip_two.setPixelColor(i, Color(0, 0, 0))
        
        self.strip_one.show()
        self.strip_two.show()

    def clear_leds(self):
        """
        Schaltet alle konfigurierten LEDs aus
        """
        for i in range(self.config.LED_PER_STRIP):
            self.strip_one.setPixelColor(i, Color(0, 0, 0))
            self.strip_two.setPixelColor(i, Color(0, 0, 0))
        
        self.strip_one.show()
        self.strip_two.show()

    def set_color(self, color):
        """
        Setzt alle LEDs auf eine bestimmte Farbe
        
        :param color: RGB-Tupel oder Hex-Farbwert
        """
        # Konvertiere Hex zu RGB, falls nötig
        if isinstance(color, str):
            color = self._hex_to_rgb(color)
        
        r, g, b = color
        
        for i in range(self.config.LED_PER_STRIP):
            self.strip_one.setPixelColor(i, Color(r, g, b))
            self.strip_two.setPixelColor(i, Color(r, g, b))
        
        self.strip_one.show()
        self.strip_two.show()

    def _hex_to_rgb(self, hex_color):
        """
        Konvertiert Hex-Farbwert zu RGB
        
        :param hex_color: Hex-Farbwert (z.B. '#3498db')
        :return: RGB-Tupel
        """
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def play_transition_animation(self):
        """
        Spielt eine kurze Übergangsanimation ab:
        Schnelles Aufblitzen aller LEDs in Regenbogenfarben und dann 0,5 Sekunden aus.
        """
        # Anzahl der Frames für die Animation
        blink_frames = 5  # Wenige Frames für schnelles Blinken
        
        # 1. Phase: Schnelles Aufblitzen mit Regenbogenfarben
        for frame in range(blink_frames):
            # Berechne Farbe basierend auf aktueller Frame-Position
            hue = frame / float(blink_frames)
            
            # Umwandlung HSV zu RGB
            if hue < 1/6:
                r, g, b = 255, int(hue * 6 * 255), 0
            elif hue < 2/6:
                r, g, b = int((2/6 - hue) * 6 * 255), 255, 0
            elif hue < 3/6:
                r, g, b = 0, 255, int((hue - 2/6) * 6 * 255)
            elif hue < 4/6:
                r, g, b = 0, int((4/6 - hue) * 6 * 255), 255
            elif hue < 5/6:
                r, g, b = int((hue - 4/6) * 6 * 255), 0, 255
            else:
                r, g, b = 255, 0, int((1 - hue) * 6 * 255)
            
            # Setze alle LEDs auf die gleiche Farbe für gleichzeitiges Blinken
            for i in range(Config.LED_PER_STRIP):
                self.strip_one.setPixelColor(i, Color(r, g, b))
                self.strip_two.setPixelColor(i, Color(r, g, b))
            
            # Aktualisiere die LED-Streifen
            self.strip_one.show()
            self.strip_two.show()
            
            # Kurze Pause für sichtbare Animation (sehr kurz für schnelles Blinken)
            time.sleep(0.05)
        
        # 2. Phase: Alle LEDs ausschalten
        for i in range(Config.LED_PER_STRIP):
            self.strip_one.setPixelColor(i, Color(0, 0, 0))
            self.strip_two.setPixelColor(i, Color(0, 0, 0))
        
        self.strip_one.show()
        self.strip_two.show()
        
        # 3. Phase: Pause von 0,5 Sekunden
        time.sleep(1)