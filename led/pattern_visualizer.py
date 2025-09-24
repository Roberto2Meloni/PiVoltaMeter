import colorsys
import time
import random
import math
from rpi_ws281x import Color
from config.config import Config
from led.manager import BaseLEDController

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
            self._visualize_ping_pong()
        elif pattern == 'static_pattern_03':
            self._visualize_dual_pulse()
        elif pattern == 'static_pattern_04':
            self._visualize_matrix_rain()
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

    def _visualize_ping_pong(self):
        """
        Zeigt eine pulsierende Animation, die sich hin und her bewegt (Ping-Pong-Effekt).
        Am Ende des LED-Streifens wechselt die Bewegungsrichtung.
        """
        # Falls noch nicht vorhanden, initialisiere die Position und Richtung für die Animation
        if not hasattr(self, '_ping_pong_position'):
            self._ping_pong_position = 0
            self._ping_pong_direction = 1  # 1 = vorwärts, -1 = rückwärts
        
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
            distance = abs(i - self._ping_pong_position)
            
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
        self._ping_pong_position += self._ping_pong_direction
        
        # Richtungswechsel am Anfang oder Ende des Streifens
        if self._ping_pong_position >= Config.LED_PER_STRIP - 1:
            self._ping_pong_direction = -1  # Wechsel zur Rückwärtsbewegung
        elif self._ping_pong_position <= 0:
            self._ping_pong_direction = 1   # Wechsel zur Vorwärtsbewegung
        
        # Kleine Pause für gleichmäßige Animation
        time.sleep(0.1)

    def _visualize_dual_pulse(self):
        """
        Zeigt eine Animation mit zwei Lichtpulsen, die von der Mitte aus starten und 
        sich in entgegengesetzte Richtungen bewegen. Wenn sie die Enden erreichen, 
        kehren sie zur Mitte zurück und treffen sich dort wieder.
        """
        # Falls noch nicht vorhanden, initialisiere die Position und Richtung für die Animation
        if not hasattr(self, '_dual_pulse_offset'):
            self._dual_pulse_offset = 0
            self._dual_pulse_direction = 1  # 1 = nach außen, -1 = zur Mitte
        
        # Alle LEDs zunächst ausschalten
        for i in range(Config.LED_PER_STRIP):
            self.strip_one.setPixelColor(i, Color(0, 0, 0))
            self.strip_two.setPixelColor(i, Color(0, 0, 0))
        
        # Mittelpunkt des LED-Streifens bestimmen
        center = Config.LED_PER_STRIP // 2
        
        # Bestimme die Position der beiden Pulse (links und rechts vom Zentrum)
        left_pulse_pos = center - self._dual_pulse_offset
        right_pulse_pos = center + self._dual_pulse_offset
        
        # Breite des Pulses in LEDs
        pulse_width = 3
        
        # Prüfe, ob Regenbogen-Modus aktiv ist
        is_rainbow = Config.LED_COLOR.lower() == 'rainbow'
        
        if not is_rainbow:
            # Normaler Farbmodus - hole die Farbe aus der Konfiguration
            color = self._get_color_from_config()
            base_r = (color >> 16) & 0xFF
            base_g = (color >> 8) & 0xFF
            base_b = color & 0xFF
        
        # Für jede LED im LED-Streifen
        for i in range(Config.LED_PER_STRIP):
            # Berechne den Abstand zu beiden Pulsen
            left_distance = abs(i - left_pulse_pos)
            right_distance = abs(i - right_pulse_pos)
            
            # Nehme die kleinste Distanz, damit der nächstgelegene Puls die Farbe bestimmt
            distance = min(left_distance, right_distance)
            
            # Wenn die LED innerhalb der Pulsbreite liegt
            if distance < pulse_width:
                # Intensität nimmt mit Abstand vom Puls-Zentrum ab
                intensity = 1.0 - (distance / pulse_width)
                
                if is_rainbow:
                    # Im Regenbogen-Modus: Farbe basierend auf Position im Strip
                    hue = i / float(Config.LED_PER_STRIP)
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
        
        # Bewege die Pulse für die nächste Aktualisierung
        self._dual_pulse_offset += self._dual_pulse_direction
        
        # Richtungswechsel an den Enden oder wenn sich die Pulse in der Mitte treffen
        max_offset = center  # Maximaler Abstand vom Zentrum
        
        if self._dual_pulse_offset >= max_offset:
            # Die Pulse haben die Enden erreicht und bewegen sich nun zur Mitte
            self._dual_pulse_direction = -1
        elif self._dual_pulse_offset <= 0:
            # Die Pulse haben sich in der Mitte getroffen und bewegen sich nun nach außen
            self._dual_pulse_direction = 1
        
        # Kleine Pause für gleichmäßige Animation
        time.sleep(0.1)
    
    def _visualize_matrix_rain(self):
        """
        Erzeugt einen Matrix-ähnlichen Regen-Effekt mit zufällig aufleuchtenden LEDs, 
        die langsam verblassen und so den Eindruck von herabfallenden Datenströmen erzeugen.
        """
        # Falls noch nicht vorhanden, initialisiere die Matrix-Datenstruktur
        if not hasattr(self, '_matrix_data'):
            # Für jede LED speichern wir die aktuelle Intensität (0-255)
            self._matrix_data = [0] * Config.LED_PER_STRIP
            self._matrix_drop_chance = 0.1  # Wahrscheinlichkeit für einen neuen "Tropfen"
        
        # Basisfarbe für den Matrix-Effekt
        base_color = Config.LED_COLOR.lower()
        
        # Bestimme die Farbwerte basierend auf der Konfiguration
        if base_color == 'rainbow':
            # Regenbogen-Modus - jede LED bekommt eine andere Farbe
            colors = []
            for i in range(Config.LED_PER_STRIP):
                hue = i / float(Config.LED_PER_STRIP)
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
                colors.append((r, g, b))
        elif base_color == 'green':
            # Klassisches Matrix-Grün für alle LEDs
            r, g, b = 0, 255, 0
        else:
            # Verwende die konfigurierte Farbe
            color = self._get_color_from_config()
            r = (color >> 16) & 0xFF
            g = (color >> 8) & 0xFF
            b = color & 0xFF
        
        # Neue "Regentropfen" mit einer bestimmten Wahrscheinlichkeit hinzufügen
        for i in range(Config.LED_PER_STRIP):
            # Zufällig neue LEDs aktivieren
            if self._matrix_data[i] == 0 and random.random() < self._matrix_drop_chance:
                self._matrix_data[i] = 255  # Neue LED mit maximaler Helligkeit
        
        # LEDs aktualisieren
        for i in range(Config.LED_PER_STRIP):
            intensity = self._matrix_data[i]
            
            if intensity > 0:
                # Bestimme die Farbe für diese LED
                if base_color == 'rainbow':
                    # Im Regenbogen-Modus: Jede LED hat ihre eigene Farbe
                    base_r, base_g, base_b = colors[i]
                else:
                    # Sonst: Standardfarbe für alle LEDs
                    base_r, base_g, base_b = r, g, b
                
                # Skaliere die Grundfarbe mit der aktuellen Intensität
                color_r = int(base_r * intensity / 255)
                color_g = int(base_g * intensity / 255)
                color_b = int(base_b * intensity / 255)
                
                # Setze die Farbe für beide LED-Streifen
                self.strip_one.setPixelColor(i, Color(color_r, color_g, color_b))
                self.strip_two.setPixelColor(i, Color(color_r, color_g, color_b))
                
                # Verringere die Intensität für den nächsten Frame (Verblassen)
                self._matrix_data[i] = max(0, intensity - random.randint(5, 15))
            else:
                # LED ist aus
                self.strip_one.setPixelColor(i, Color(0, 0, 0))
                self.strip_two.setPixelColor(i, Color(0, 0, 0))
        
        # Aktualisiere die LED-Streifen
        self.strip_one.show()
        self.strip_two.show()
        
        # Kleine Pause für die Animation
        time.sleep(0.05)