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

# only_led.py
# import time
# import random
# from rpi_ws281x import PixelStrip, Color
# import pyaudio
# import numpy as np
# from config.config import Config


# # Initialisierung der LED-Streifen
# strip_one = PixelStrip(Config.LED_PER_STRIP, Config.LED_PIN_ONE, Config.LED_FREQ_HZ, Config.LED_DMA_ONE, Config.LED_INVERT, Config.LED_BRIGHTNESS, Config.LED_CHANNEL_ONE)
# strip_two = PixelStrip(Config.LED_PER_STRIP, Config.LED_PIN_TWO, Config.LED_FREQ_HZ, Config.LED_DMA_TWO, Config.LED_INVERT, Config.LED_BRIGHTNESS, Config.LED_CHANNEL_TWO)

# strip_one.begin()
# strip_two.begin()  # Strip zwei starten

# def random_color():
#     """Erzeugt eine zufällige RGB-Farbe"""
#     return Color(
#         random.randint(0, 255),  # R
#         random.randint(0, 255),  # G
#         random.randint(0, 255)   # B
#     )



# def start_phase_one():
#     """Start-Animation: LEDs werden nacheinander mit zufälligen Farben eingeschaltet"""
#     print("Starte die Einschaltsequenz 1...")
    
#     # Zuerst alle LEDs ausschalten
#     for i in range(Config.LED_PER_STRIP):
#         strip_one.setPixelColor(i, Color(0, 0, 0))
#         strip_two.setPixelColor(i, Color(0, 0, 0))
#     strip_one.show()
#     strip_two.show()
    
    
#     # Schalte LEDs nacheinander ein
#     for i in range(Config.LED_PER_STRIP):
#         # Setze eine zufällige Farbe für diese LED
#         strip_one.setPixelColor(i, random_color())
#         strip_two.setPixelColor(i, random_color())
        
#         # Aktualisiere die LED-Anzeige
#         strip_one.show()
#         strip_two.show()
        
#         # Warte 0.1 Sekunden vor der nächsten LED
#         time.sleep(0.1)
    
#     print(f"{Config.LED_PER_STRIP} LEDs wurden aktiviert.")


    
#     # Dann schalten wir sie aus
#     print("Schalte alle LEDs aus...")
#     for i in range(Config.LED_PER_STRIP ):
#         strip_one.setPixelColor(i, Color(0, 0, 0))
#         strip_two.setPixelColor(i, Color(0, 0, 0))
#         strip_one.show()  # Diese Zeile muss innerhalb der Schleife sein
#         strip_two.show()  # Diese Zeile muss innerhalb der Schleife sein
#         time.sleep(0.1)   # Verzögerung für den Animationseffekt

# def start_all_start_phase():
#     start_phase_one()


# def animation_webserver_starting(iterations=1):
#     """
#     Animation beim Starten des Webservers - blaues sequentielles Ein- und Ausschalten
#     iterations: Anzahl der Durchläufe (Standard: 1, für Endlosschleife -1 verwenden)
#     """
#     print("Webserver wird gestartet - Animation läuft...")
    
#     count = 0
#     while iterations == -1 or count < iterations:
#         count += 1
        
#         # Alle LEDs ausschalten
#         for i in range(Config.LED_PER_STRIP):
#             strip_one.setPixelColor(i, Color(0, 0, 0))
#             strip_two.setPixelColor(i, Color(0, 0, 0))
#         strip_one.show()
#         strip_two.show()
        
#         # Blaues Licht sequentiell einschalten (von LED 1 bis zur letzten)
#         for i in range(Config.LED_PER_STRIP):
#             # Setze aktuelle LED auf Blau
#             strip_one.setPixelColor(i, Color(0, 0, 255))  # Blau
#             strip_two.setPixelColor(i, Color(0, 0, 255))  # Blau
            
#             # Aktualisiere die LED-Anzeige
#             strip_one.show()
#             strip_two.show()
            
#             # Kurze Pause
#             time.sleep(0.1)
        
#         # Kurze Pause, wenn alle LEDs eingeschaltet sind
#         time.sleep(0.3)
        
#         # Blaues Licht sequentiell ausschalten (von LED 1 bis zur letzten)
#         for i in range(Config.LED_PER_STRIP):
#             # Setze aktuelle LED aus
#             strip_one.setPixelColor(i, Color(0, 0, 0))  # Aus
#             strip_two.setPixelColor(i, Color(0, 0, 0))  # Aus
            
#             # Aktualisiere die LED-Anzeige
#             strip_one.show()
#             strip_two.show()
            
#             # Kurze Pause
#             time.sleep(0.1)



# def animation_webserver_error(loop=True):
#     """Animation wenn der Webserver nicht gestartet werden konnte - rotes Blinken"""
#     print("Webserver-Fehler - Animation läuft...")
    
#     # Anzahl der Durchläufe
#     cycles = 1000 if loop else 5  # Wenn loop=True, dann quasi endlos, sonst 5 Zyklen
    
#     for _ in range(cycles):
#         # Alle LEDs rot
#         for i in range(Config.LED_PER_STRIP):
#             strip_one.setPixelColor(i, Color(255, 0, 0))  # Rot
#             strip_two.setPixelColor(i, Color(255, 0, 0))  # Rot
#         strip_one.show()
#         strip_two.show()
#         time.sleep(0.5)
        
#         # Alle LEDs aus
#         for i in range(Config.LED_PER_STRIP):
#             strip_one.setPixelColor(i, Color(0, 0, 0))  # Aus
#             strip_two.setPixelColor(i, Color(0, 0, 0))  # Aus
#         strip_one.show()
#         strip_two.show()
#         time.sleep(0.5)


# def pulsing_all_led(color_hex, cycles=3):
#     """
#     Lässt alle LEDs in der angegebenen Farbe pulsieren
    
#     Parameter:
#     color_hex (str): Hexadezimaler Farbwert (z.B. "#FF0000" für Rot)
#     cycles (int): Anzahl der Pulsier-Zyklen
#     """
#     print(f"Pulsieren in Farbe {color_hex}...")
    
#     # Hexwert in RGB-Komponenten umwandeln
#     color_hex = color_hex.lstrip('#')
#     r = int(color_hex[0:2], 16)
#     g = int(color_hex[2:4], 16)
#     b = int(color_hex[4:6], 16)
    
#     # Mehrere Pulsier-Zyklen durchführen
#     for _ in range(cycles):
#         # Helligkeit erhöhen (0% bis 100%)
#         for brightness in range(0, 101, 2):
#             brightness_factor = brightness / 100.0
            
#             # Aktuelle Farbwerte berechnen
#             current_r = int(r * brightness_factor)
#             current_g = int(g * brightness_factor)
#             current_b = int(b * brightness_factor)
            
#             # Alle LEDs auf aktuelle Farbe setzen
#             for i in range(Config.LED_PER_STRIP):
#                 strip_one.setPixelColor(i, Color(current_r, current_g, current_b))
#                 strip_two.setPixelColor(i, Color(current_r, current_g, current_b))
            
#             # LED-Streifen aktualisieren
#             strip_one.show()
#             strip_two.show()
            
#             # Kurze Pause
#             time.sleep(0.01)
        
#         # Kurze Pause bei voller Helligkeit
#         time.sleep(0.2)
        
#         # Helligkeit verringern (100% bis 0%)
#         for brightness in range(100, -1, -2):
#             brightness_factor = brightness / 100.0
            
#             # Aktuelle Farbwerte berechnen
#             current_r = int(r * brightness_factor)
#             current_g = int(g * brightness_factor)
#             current_b = int(b * brightness_factor)
            
#             # Alle LEDs auf aktuelle Farbe setzen
#             for i in range(Config.LED_PER_STRIP):
#                 strip_one.setPixelColor(i, Color(current_r, current_g, current_b))
#                 strip_two.setPixelColor(i, Color(current_r, current_g, current_b))
            
#             # LED-Streifen aktualisieren
#             strip_one.show()
#             strip_two.show()
            
#             # Kurze Pause
#             time.sleep(0.01)
        
#         # Kurze Pause bei 0% Helligkeit
#         time.sleep(0.2)
    
#     # Alle LEDs ausschalten
#     for i in range(Config.LED_PER_STRIP):
#         strip_one.setPixelColor(i, Color(0, 0, 0))
#         strip_two.setPixelColor(i, Color(0, 0, 0))
#     strip_one.show()
#     strip_two.show()



# def audio_visualizer():
#     # Audio-Parameter
#     FORMAT = pyaudio.paInt16
#     CHANNELS = 1
#     RATE = 44100
#     CHUNK = 1024
    
#     # Verwende einen Glättungsfaktor für flüssigere Übergänge
#     smoothing = 0.3  # Niedrigerer Wert = weniger Glättung, höherer Wert = mehr Glättung
#     last_amplitude = 0
    
#     p = pyaudio.PyAudio()
    
#     # Geräteinformationen ausgeben
#     print("Verfügbare Audiogeräte:")
#     for i in range(p.get_device_count()):
#         dev_info = p.get_device_info_by_index(i)
#         print(f"Device {i}: {dev_info['name']}")
#         print(f"  Max Input Channels: {dev_info['maxInputChannels']}")
#         print(f"  Default Sample Rate: {dev_info['defaultSampleRate']}")
    
#     # Finde das erste Eingabegerät
#     device_index = None
#     for i in range(p.get_device_count()):
#         dev_info = p.get_device_info_by_index(i)
#         if dev_info['maxInputChannels'] > 0:
#             device_index = i
#             break
    
#     if device_index is None:
#         print("Kein Eingabegerät gefunden!")
#         return
    
#     try:
#         print(f"Öffne Audiogerät {device_index}...")
#         stream = p.open(format=FORMAT,
#                        channels=CHANNELS,
#                        rate=RATE,
#                        input=True,
#                        input_device_index=device_index,
#                        frames_per_buffer=CHUNK)
        
#         print("Audio-Visualisierung gestartet... (Drücken Sie Strg+C zum Beenden)")
        
#         while True:
#             # Lese Audiodaten
#             data = stream.read(CHUNK, exception_on_overflow=False)
            
#             # Konvertiere zu numpy array
#             audio_data = np.frombuffer(data, dtype=np.int16)
            
#             # Sichere Berechnung der RMS-Amplitude
#             if len(audio_data) > 0 and np.any(np.isfinite(audio_data)):
#                 # Berechne RMS-Amplitude
#                 amplitude_rms = np.sqrt(np.mean(np.square(audio_data.astype(float))))
                
#                 # Normalisiere auf Bereich 0-100
#                 amplitude_scaled = min(100, int(amplitude_rms / 32768 * 100))
                
#                 # Wende Glättung an
#                 smoothed_amplitude = last_amplitude * smoothing + amplitude_scaled * (1 - smoothing)
#                 last_amplitude = smoothed_amplitude
                
#                 # Visualisiere in Konsole
#                 bar = '#' * int(smoothed_amplitude / 2)
#                 print(f"Amplitude: {smoothed_amplitude:3.1f}/100 |{bar:<50}|", end='\r')
                
#                 # Berechne, wie viele LEDs leuchten sollen
#                 num_leds = int(smoothed_amplitude / 100 * Config.LED_PER_STRIP)
                
#                 # Aktualisiere LEDs
#                 for i in range(Config.LED_PER_STRIP):
#                     if i < num_leds:
#                         # Farbverlauf von Grün zu Rot
#                         hue = (120 - (i * 120 / Config.LED_PER_STRIP)) / 360.0
#                         r, g, b = [int(x * 255) for x in hsv_to_rgb(hue, 1.0, 1.0)]
#                         strip_one.setPixelColor(i, Color(r, g, b))
#                         strip_two.setPixelColor(i, Color(r, g, b))
#                     else:
#                         strip_one.setPixelColor(i, Color(0, 0, 0))
#                         strip_two.setPixelColor(i, Color(0, 0, 0))
                
#                 strip_one.show()
#                 strip_two.show()
#             else:
#                 print("Keine gültigen Audiodaten gefunden.", end='\r')
    
#     except KeyboardInterrupt:
#         print("\nBeendet.")
#     except Exception as e:
#         print(f"\nFehler: {e}")
#         import traceback
#         traceback.print_exc()
#     finally:
#         if 'stream' in locals():
#             stream.stop_stream()
#             stream.close()
#         p.terminate()
        
#         # Alle LEDs ausschalten
#         for i in range(Config.LED_PER_STRIP):
#             strip_one.setPixelColor(i, Color(0, 0, 0))
#             strip_two.setPixelColor(i, Color(0, 0, 0))
#         strip_one.show()
#         strip_two.show()