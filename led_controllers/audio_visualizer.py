import pyaudio
import numpy as np
from rpi_ws281x import Color
from .base_controller import BaseLEDController
from config.config import Config

class AudioVisualizer(BaseLEDController):
    def __init__(self, config=None):
        """
        Initialisiert den Audio-Visualisierer
        
        :param config: Konfigurationsobjekt (optional)
        """
        super().__init__(config)
        self.config = config or Config
        self.last_amplitude = 0
        self.audio_stream = None
        self.pyaudio_instance = None

    def _hsv_to_rgb(self, h, s, v):
        """
        Konvertiert HSV-Farbwerte in RGB
        
        :param h: Farbton (0-1)
        :param s: Sättigung (0-1)
        :param v: Helligkeit (0-1)
        :return: RGB-Tupel
        """
        if s == 0.0:
            return v, v, v
        
        i = int(h * 6)
        f = (h * 6) - i
        p = v * (1 - s)
        q = v * (1 - s * f)
        t = v * (1 - s * (1 - f))
        
        if i % 6 == 0:
            return v, t, p
        elif i % 6 == 1:
            return q, v, p
        elif i % 6 == 2:
            return p, v, t
        elif i % 6 == 3:
            return p, q, v
        elif i % 6 == 4:
            return t, p, v
        else:
            return v, p, q

    def _get_input_device(self):
        """
        Findet das erste verfügbare Eingabegerät
        
        :return: Index des Eingabegeräts
        """
        p = pyaudio.PyAudio()
        for i in range(p.get_device_count()):
            dev_info = p.get_device_info_by_index(i)
            if dev_info['maxInputChannels'] > 0:
                return i
        return None

    def start_visualization(self):
        """
        Startet die Audio-Visualisierung
        """
        print("Starte Audio-Visualisierung...")
        
        # Audio-Parameter
        FORMAT = pyaudio.paInt16
        CHANNELS = self.config.AUDIO_CHANNELS
        RATE = self.config.AUDIO_RATE
        CHUNK = self.config.AUDIO_CHUNK
        
        # PyAudio-Instanz erstellen
        self.pyaudio_instance = pyaudio.PyAudio()
        
        # Eingabegerät finden
        device_index = self._get_input_device()
        
        if device_index is None:
            print("Kein Eingabegerät gefunden!")
            return
        
        try:
            # Audio-Stream öffnen
            self.audio_stream = self.pyaudio_instance.open(
                format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                input_device_index=device_index,
                frames_per_buffer=CHUNK
            )
            
            print("Audio-Visualisierung läuft... (Strg+C zum Beenden)")
            
            while True:
                # Audiodaten lesen
                data = self.audio_stream.read(CHUNK, exception_on_overflow=False)
                
                # Daten zu numpy-Array konvertieren
                audio_data = np.frombuffer(data, dtype=np.int16)
                
                # Sicherstellen, dass Daten gültig sind
                if len(audio_data) > 0 and np.any(np.isfinite(audio_data)):
                    # RMS-Amplitude berechnen
                    amplitude_rms = np.sqrt(np.mean(np.square(audio_data.astype(float))))
                    
                    # Auf Bereich 0-100 skalieren
                    amplitude_scaled = min(100, int(amplitude_rms / 32768 * 100))
                    
                    # Glättung anwenden
                    smoothed_amplitude = (
                        self.last_amplitude * self.config.AUDIO_SMOOTHING + 
                        amplitude_scaled * (1 - self.config.AUDIO_SMOOTHING)
                    )
                    self.last_amplitude = smoothed_amplitude
                    
                    # LEDs basierend auf Amplitude aktualisieren
                    self._update_leds(smoothed_amplitude)
                    
                else:
                    print("Keine gültigen Audiodaten gefunden.", end='\r')
        
        except KeyboardInterrupt:
            print("\nBeendet.")
        except Exception as e:
            print(f"\nFehler: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.stop_visualization()

    def stop_visualization(self):
        """
        Stoppt die Audio-Visualisierung und räumt Ressourcen auf
        """
        if self.audio_stream:
            self.audio_stream.stop_stream()
            self.audio_stream.close()
        
        if self.pyaudio_instance:
            self.pyaudio_instance.terminate()
        
        # Alle LEDs ausschalten
        self.clear_leds()
            
    def _update_leds(self, amplitude):
        # Berechnen, wie viele LEDs leuchten sollen
        num_leds = int(amplitude / 100 * self.config.LED_PER_STRIP)
        
        # Farbmodus auswählen
        if self.config.AMPLITUDE_COLOR_MODE == 'fixed':
            # Festgelegte Farbe verwenden
            color_hex = self.config.FIXED_AMPLITUDE_COLOR.lstrip('#')
            r = int(color_hex[0:2], 16)
            g = int(color_hex[2:4], 16)
            b = int(color_hex[4:6], 16)
            
            for i in range(self.config.LED_PER_STRIP):
                if i < num_leds:
                    # Festgelegte Farbe für alle LEDs
                    self.strip_one.setPixelColor(i, Color(r, g, b))
                    self.strip_two.setPixelColor(i, Color(r, g, b))
                else:
                    # Ausschalten für nicht benötigte LEDs
                    self.strip_one.setPixelColor(i, Color(0, 0, 0))
                    self.strip_two.setPixelColor(i, Color(0, 0, 0))
        else:
            # Ursprünglicher Farbverlauf
            for i in range(self.config.LED_PER_STRIP):
                if i < num_leds:
                    # Farbverlauf von Grün zu Rot
                    hue = (120 - (i * 120 / self.config.LED_PER_STRIP)) / 360.0
                    r, g, b = [int(x * 255) for x in self._hsv_to_rgb(hue, 1.0, 1.0)]
                    
                    # Setze Farbe für beide Streifen
                    self.strip_one.setPixelColor(i, Color(r, g, b))
                    self.strip_two.setPixelColor(i, Color(r, g, b))
                else:
                    # Ausschalten für nicht benötigte LEDs
                    self.strip_one.setPixelColor(i, Color(0, 0, 0))
                    self.strip_two.setPixelColor(i, Color(0, 0, 0))
        
        # Aktualisiere LED-Streifen
        self.strip_one.show()
        self.strip_two.show()