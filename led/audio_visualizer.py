import time
import random
import numpy as np
import pyaudio
from rpi_ws281x import Color
from config.config import Config
from led.manager import BaseLEDController

class AudioVisualizer(BaseLEDController):
    def __init__(self):
        """Initialisiert den Audio-Visualizer mit Audioverarbeitung"""
        super().__init__()
        
        # Audioverarbeitungs-Parameter
        self.CHUNK = 1024  # Anzahl der Audio-Samples pro Frame
        self.FORMAT = pyaudio.paInt16  # Audio-Format
        self.CHANNELS = Config.audio_channels  # Stereo
        self.RATE = 44100  # Sampling-Rate in Hz
        
        # PyAudio-Instanz initialisieren
        self.p = pyaudio.PyAudio()
        self.stream = None
        
        # Parameter für die Visualisierung
        self.amplitude_smooth_left = 0  # Geglätteter Amplitudenwert für linken Kanal
        self.amplitude_smooth_right = 0  # Geglätteter Amplitudenwert für rechten Kanal
        self.smoothing_factor = 0.3  # Glättungsfaktor für flüssigere Übergänge
        
        # Audiostream starten
        self._start_audio_stream()
    
    def _start_audio_stream(self):
        """Startet den Audio-Stream für die Echtzeit-Analyse mit automatischer Geräteerkennung"""
        try:
            # Liste verfügbare Geräte auf
            info = self.p.get_host_api_info_by_index(0)
            num_devices = info.get('deviceCount')
            
            # Ausgabe der verfügbaren Geräte für Debugging
            print(f"Verfügbare Audiogeräte: {num_devices}")
            
            # Standardgerät finden, das mindestens 1 Eingangskanal hat
            default_device_index = None
            max_input_channels = 0
            
            for i in range(num_devices):
                device_info = self.p.get_device_info_by_index(i)
                input_channels = int(device_info.get('maxInputChannels', 0))
                
                print(f"Gerät {i}: {device_info.get('name')}, Eingangskanäle: {input_channels}")
                
                # Suche nach dem Gerät mit den meisten Eingangskanälen
                if input_channels > max_input_channels:
                    max_input_channels = input_channels
                    default_device_index = i
            
            if default_device_index is None or max_input_channels == 0:
                print("Kein geeignetes Audiogerät gefunden! Verwende simulierte Daten.")
                self.stream = None
                return
                
            # Bestimme die maximale Anzahl an Kanälen (1 für Mono, 2 für Stereo)
            channel_count = min(2, max_input_channels)
            self.CHANNELS = channel_count  # Update der Klassenattribute
            
            device_info = self.p.get_device_info_by_index(default_device_index)
            print(f"Verwende Audiogerät: {device_info.get('name')} mit {channel_count} Kanal(en)")
            
            # Stream mit der korrekten Kanalanzahl erstellen
            self.stream = self.p.open(
                format=self.FORMAT,
                channels=channel_count,
                rate=self.RATE,
                input=True,
                input_device_index=default_device_index,
                frames_per_buffer=self.CHUNK
            )
            
            print(f"Audiostream erfolgreich gestartet mit {channel_count} Kanal(en)")
            
        except Exception as e:
            print(f"Fehler beim Starten des Audiostreams: {e}")
            # Fallback auf simulierte Werte
            self.stream = None
    
    def update(self):
        """
        Aktualisiert die LED-Anzeige basierend auf der Audioamplitude.
        Diese Methode wird regelmäßig vom LED-Manager aufgerufen.
        """
        # Bestimme das aktuelle Muster aus der Config
        pattern = Config.AUDIO_PATTERN
        
        # Audioamplitude erfassen (diese Methode aktualisiert bereits amplitude_smooth_left und amplitude_smooth_right)
        amplitude_percent = self._get_audio_amplitude()
        
        # Aktualisiere Animation basierend auf dem Muster
        if pattern == 'audio_pattern_01':
            self._visualize_mono_vu_meter(amplitude_percent)
        elif pattern == 'audio_pattern_02':
            self._visualize_mono_pulse(amplitude_percent)
        elif pattern == 'audio_pattern_03':
            self._visualize_mono_center_bloom(amplitude_percent)
        elif pattern == 'audio_pattern_04':
            # Neues Stereo-Muster
            self._visualize_stereo_vu_meter()
        elif pattern == 'audio_pattern_05':
            # Neues Stereo-Muster
            self._visualize_stereo_pulse()
        elif pattern == 'audio_pattern_06':
            # Neues Stereo-Muster
            self._visualize_stereo_center_bloom()
        else:
            # Fallback: Audioreaktive Volltonfarbe
            self._visualize_reactive_solid_color(amplitude_percent)
    
    def _get_audio_amplitude(self):
        """
        Erfasst die aktuelle Audioamplitude und gibt sie als Prozentwert zurück.
        Bei Problemen mit dem Audiostream wird ein simulierter Wert zurückgegeben.
        
        Bei Stereo-Signalen werden linker und rechter Kanal getrennt verarbeitet.
        """
        if self.stream:
            try:
                # Audiodaten vom Stream lesen
                data = self.stream.read(self.CHUNK, exception_on_overflow=False)
                # Umwandlung in NumPy-Array
                audio_data = np.frombuffer(data, dtype=np.int16)
                
                # Zum Loggen
                # print(audio_data)
                
                # Stereo-Daten separieren in linken und rechten Kanal
                if self.CHANNELS == 2:
                    # Linker Kanal (gerade Indizes)
                    left_channel = audio_data[0::2]
                    # Rechter Kanal (ungerade Indizes)
                    right_channel = audio_data[1::2]
                    
                    # Berechne RMS für jeden Kanal
                    rms_left = np.sqrt(np.mean(np.square(left_channel)))
                    rms_right = np.sqrt(np.mean(np.square(right_channel)))
                    
                    # Normalisiere auf Prozentwerte (0-100%)
                    max_possible_amplitude = 32768.0
                    
                    current_amplitude_left = min(100, (rms_left / max_possible_amplitude) * 100 * 5)  # Verstärkungsfaktor 5
                    current_amplitude_right = min(100, (rms_right / max_possible_amplitude) * 100 * 5)  # Verstärkungsfaktor 5
                    
                    # Glätte die Werte für sanftere Übergänge
                    self.amplitude_smooth_left = self.smoothing_factor * current_amplitude_left + (1 - self.smoothing_factor) * self.amplitude_smooth_left
                    self.amplitude_smooth_right = self.smoothing_factor * current_amplitude_right + (1 - self.smoothing_factor) * self.amplitude_smooth_right
                    
                    # Ausgabe der Amplituden in der Konsole
                    # print(f"Audio-Amplitude: Links: {self.amplitude_smooth_left:.2f}% | Rechts: {self.amplitude_smooth_right:.2f}%")
                    
                    # Durchschnitt für Funktionen zurückgeben, die nur einen Wert verwenden
                    return (self.amplitude_smooth_left + self.amplitude_smooth_right) / 2
                
                else:  # Mono-Verarbeitung als Fallback
                    # Berechne die RMS-Amplitude (Root Mean Square)
                    rms = np.sqrt(np.mean(np.square(audio_data)))
                    
                    # Normalisiere auf einen Prozentwert (0-100%)
                    max_possible_amplitude = 32768.0
                    current_amplitude = min(100, (rms / max_possible_amplitude) * 100 * 5)  # Verstärkungsfaktor 5
                    
                    # Setze beide Kanäle auf den gleichen Wert
                    self.amplitude_smooth_left = self.amplitude_smooth_right = self.smoothing_factor * current_amplitude + (1 - self.smoothing_factor) * self.amplitude_smooth_left
                    
                    print(f"Audio-Amplitude (Mono): {self.amplitude_smooth_left:.2f}%")
                    
                    return self.amplitude_smooth_left
                
            except Exception as e:
                print(f"Fehler bei der Audioerfassung: {e}")
                return self._simulate_audio_amplitude()
        else:
            # Fallback auf simulierte Werte
            return self._simulate_audio_amplitude()
    
    def _simulate_audio_amplitude(self):
        """
        Simuliert eine Audioamplitude für den Fall, dass keine echte Audioquelle vorhanden ist.
        Gibt für Stereo zwei leicht unterschiedliche Werte zurück.
        """
        # Einfache Simulation mit etwas Zufall für einen natürlicheren Effekt
        base_amplitude = 30
        time_factor = abs(np.sin(time.time() * 2)) 
        
        # Leicht unterschiedliche Werte für linken und rechten Kanal
        random_left = 40 * time_factor + random.uniform(0, 30)
        random_right = 40 * time_factor + random.uniform(0, 30) * 0.8  # Leicht andere Charakteristik
        
        # Werte speichern
        self.amplitude_smooth_left = min(100, base_amplitude + random_left)
        self.amplitude_smooth_right = min(100, base_amplitude + random_right)
        
        # Ausgabe der simulierten Amplituden
        # print(f"Simulierte Audio-Amplitude: Links: {self.amplitude_smooth_left:.2f}% | Rechts: {self.amplitude_smooth_right:.2f}%")
        
        # Durchschnitt für Einzelwert-Funktionen zurückgeben
        return (self.amplitude_smooth_left + self.amplitude_smooth_right) / 2
    
    def configure_from_config(self):
        """
        Konfiguriert den Controller basierend auf der aktuellen Config.
        """
        # Helligkeit setzen
        brightness = Config.LED_BRIGHTNESS
        self.strip_one.setBrightness(brightness)
        self.strip_two.setBrightness(brightness)
    
    def cleanup(self):
        """
        Bereinigt Ressourcen und bereitet den Controller auf das Beenden vor.
        """
        # Audio-Stream schließen
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        
        # PyAudio-Instanz beenden
        self.p.terminate()
        
        # LEDs ausschalten
        self.clear_all_leds()
    
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
    
    def _get_rainbow_color(self, position, intensity=255):
        """
        Erzeugt eine Regenbogenfarbe basierend auf der Position (0.0 - 1.0)
        und der Intensität (0-255).
        """
        position = position * 6  # Skalieren auf 6 Farbbereiche
        
        # Berechne Farbkomponenten
        if position < 1:
            r, g, b = 255, int(position * 255), 0
        elif position < 2:
            r, g, b = int((2 - position) * 255), 255, 0
        elif position < 3:
            r, g, b = 0, 255, int((position - 2) * 255)
        elif position < 4:
            r, g, b = 0, int((4 - position) * 255), 255
        elif position < 5:
            r, g, b = int((position - 4) * 255), 0, 255
        else:
            r, g, b = 255, 0, int((6 - position) * 255)
        
        # Intensität anwenden
        r = int(r * intensity / 255)
        g = int(g * intensity / 255)
        b = int(b * intensity / 255)
        
        return Color(r, g, b)
    
    def clear_all_leds(self):
        """
        Schaltet alle LEDs aus
        """
        print("Schalte alle LEDs aus")
        
        max_leds = max(Config.LED_PER_STRIP, 30)  # Sicherstellen, dass alle LEDs erreicht werden
        
        # Alle LEDs auf Schwarz setzen
        for i in range(max_leds):
            self.strip_one.setPixelColor(i, Color(0, 0, 0))
            self.strip_two.setPixelColor(i, Color(0, 0, 0))
        
        # Strips aktualisieren
        self.strip_one.show()
        self.strip_two.show()
    
    # Muster 1: VU-Meter-ähnliche Visualisierung
    def _visualize_mono_vu_meter(self, amplitude_percent):
        """
        Visualisiert die Audioamplitude als VU-Meter.
        Bei höherer Amplitude leuchten mehr LEDs.
        """
        # Berechne, wie viele LEDs basierend auf der Amplitude leuchten sollen
        num_leds = int((amplitude_percent / 100.0) * Config.LED_PER_STRIP)
        base_color = self._get_color_from_config()
        
        # Setze die LEDs entsprechend der Amplitude
        for i in range(Config.LED_PER_STRIP):
            if i < num_leds:
                # Farbe basierend auf Position - rot für hohe Pegel, grün für niedrige
                if Config.LED_COLOR.lower() == 'rainbow':
                    # Hellere Farben für aktivierte LEDs
                    pos = i / float(Config.LED_PER_STRIP)
                    color = self._get_rainbow_color(pos)
                else:
                    # Bei anderen Farben: Helligkeit basierend auf Position
                    intensity = min(255, int(255 * (0.5 + 0.5 * i / Config.LED_PER_STRIP)))
                    r = min(255, int((base_color >> 16) & 0xFF))
                    g = min(255, int((base_color >> 8) & 0xFF))
                    b = min(255, int(base_color & 0xFF))
                    color = Color(r, g, b)
            else:
                # Ausgeschaltete LEDs
                color = Color(0, 0, 0)
            
            self.strip_one.setPixelColor(i, color)
            self.strip_two.setPixelColor(i, color)
        
        self.strip_one.show()
        self.strip_two.show()
    
    # Muster 2: Pulsierender Effekt
    def _visualize_mono_pulse(self, amplitude_percent):
        """
        Visualisiert die Audioamplitude als pulsierender Effekt.
        Die gesamte LED-Leiste pulst mit der Musik.
        """
        # Nutze die Amplitude, um die Helligkeit zu steuern
        brightness = int((amplitude_percent / 100.0) * 255)
        
        # Farbe basierend auf Config
        base_color = self._get_color_from_config()
        
        # Skala für RGB-Werte basierend auf Amplitude
        scale = max(0.1, amplitude_percent / 100.0)
        
        for i in range(Config.LED_PER_STRIP):
            if Config.LED_COLOR.lower() == 'rainbow':
                # Rainbow-Effekt mit amplitudenabhängiger Helligkeit
                hue = (i / float(Config.LED_PER_STRIP) + time.time() * 0.1) % 1.0
                color = self._get_rainbow_color(hue, brightness)
            else:
                # Skaliere die Farbe basierend auf der Amplitude
                r = min(255, int(((base_color >> 16) & 0xFF) * scale))
                g = min(255, int(((base_color >> 8) & 0xFF) * scale))
                b = min(255, int((base_color & 0xFF) * scale))
                color = Color(r, g, b)
            
            self.strip_one.setPixelColor(i, color)
            self.strip_two.setPixelColor(i, color)
        
        self.strip_one.show()
        self.strip_two.show()
    
    # Muster 3: Symmetrisches zentrales Muster
    def _visualize_mono_center_bloom(self, amplitude_percent):
        """
        Visualisiert die Audioamplitude als symmetrisches Muster, 
        das von der Mitte nach außen wächst.
        """
        # Berechne, wie viele LEDs insgesamt leuchten sollen (von der Mitte aus)
        center = Config.LED_PER_STRIP // 2
        radius = int((amplitude_percent / 100.0) * (Config.LED_PER_STRIP // 2))
        
        # Setze alle LEDs zunächst auf aus
        for i in range(Config.LED_PER_STRIP):
            self.strip_one.setPixelColor(i, Color(0, 0, 0))
            self.strip_two.setPixelColor(i, Color(0, 0, 0))
        
        # Setze die LEDs symmetrisch um die Mitte
        for offset in range(radius + 1):
            # Berechne Position links und rechts vom Zentrum
            left = center - offset
            right = center + offset
            
            # Intensität basierend auf Entfernung vom Zentrum
            intensity = 255 - int(255 * (offset / (Config.LED_PER_STRIP / 2)))
            intensity = max(50, intensity)
            
            if Config.LED_COLOR.lower() == 'rainbow':
                # Zeit-basierte Farbänderung für pulsierenden Regenbogeneffekt
                hue = (offset / float(Config.LED_PER_STRIP) + time.time() * 0.2) % 1.0
                color = self._get_rainbow_color(hue, intensity)
            else:
                base_color = self._get_color_from_config()
                # Skaliere die Farbe basierend auf der Intensität
                r = min(255, int(((base_color >> 16) & 0xFF) * intensity / 255))
                g = min(255, int(((base_color >> 8) & 0xFF) * intensity / 255))
                b = min(255, int((base_color & 0xFF) * intensity / 255))
                color = Color(r, g, b)
            
            # Setze die Farben links und rechts vom Zentrum
            if 0 <= left < Config.LED_PER_STRIP:
                self.strip_one.setPixelColor(left, color)
                self.strip_two.setPixelColor(left, color)
            
            if 0 <= right < Config.LED_PER_STRIP and right != left:
                self.strip_one.setPixelColor(right, color)
                self.strip_two.setPixelColor(right, color)
        
        self.strip_one.show()
        self.strip_two.show()
    
    # Hilfsmuster: Reaktive Volltonfarbe
    def _visualize_reactive_solid_color(self, amplitude_percent):
        """
        Zeigt eine einheitliche Farbe an, deren Helligkeit von der Audioamplitude abhängt.
        """
        # Nutze die Amplitude, um die Helligkeit zu steuern
        brightness = int((amplitude_percent / 100.0) * 255)
        brightness = max(10, brightness)  # Minimale Helligkeit
        
        # Farbe basierend auf Config mit amplitudenabhängiger Helligkeit
        base_color = self._get_color_from_config()
        scale = max(0.1, amplitude_percent / 100.0)
        
        r = min(255, int(((base_color >> 16) & 0xFF) * scale))
        g = min(255, int(((base_color >> 8) & 0xFF) * scale))
        b = min(255, int((base_color & 0xFF) * scale))
        color = Color(r, g, b)
        
        # Setze alle LEDs auf die gleiche Farbe
        for i in range(Config.LED_PER_STRIP):
            self.strip_one.setPixelColor(i, color)
            self.strip_two.setPixelColor(i, color)
        
        self.strip_one.show()
        self.strip_two.show()
        
    # Neues Stereo-Muster
    def _visualize_stereo_vu_meter(self):
        """
        Stereo-Visualisierung: Linker und rechter Kanal werden separat auf den LED-Strips angezeigt.
        Strip_one zeigt den linken Kanal, strip_two zeigt den rechten Kanal.
        """
        # Aktuelle Amplituden für linken und rechten Kanal
        left_amplitude = self.amplitude_smooth_left
        right_amplitude = self.amplitude_smooth_right

        # Berechne, wie viele LEDs pro Strip basierend auf der Amplitude leuchten sollen
        left_leds = int((left_amplitude / 100.0) * Config.LED_PER_STRIP)
        right_leds = int((right_amplitude / 100.0) * Config.LED_PER_STRIP)
        
        # Farben für jeden Kanal definieren - unterschiedliche Farben für Links/Rechts
        base_color = self._get_color_from_config()
        
        # Spezielle Behandlung für den Regenbogenmodus
        if Config.LED_COLOR.lower() == 'rainbow':
            # Linker Kanal: Blau-zu-Rot Spektrum (kühle zu warmen Farben)
            for i in range(Config.LED_PER_STRIP):
                if i < left_leds:
                    # Farbverlauf von blau (niedrig) zu rot (hoch)
                    pos = i / float(Config.LED_PER_STRIP)
                    hue = 0.7 - pos * 0.7  # 0.7 (blau) bis 0.0 (rot)
                    intensity = min(255, int(255 * (0.5 + 0.5 * i / Config.LED_PER_STRIP)))
                    color = self._get_rainbow_color(hue, intensity)
                else:
                    color = Color(0, 0, 0)  # Aus
                self.strip_one.setPixelColor(i, color)
            
            # Rechter Kanal: Grün-zu-Gelb Spektrum
            for i in range(Config.LED_PER_STRIP):
                if i < right_leds:
                    # Farbverlauf von grün (niedrig) zu gelb (hoch)
                    pos = i / float(Config.LED_PER_STRIP)
                    hue = 0.3 - pos * 0.15  # 0.3 (grün) bis 0.15 (gelb)
                    intensity = min(255, int(255 * (0.5 + 0.5 * i / Config.LED_PER_STRIP)))
                    color = self._get_rainbow_color(hue, intensity)
                else:
                    color = Color(0, 0, 0)  # Aus
                self.strip_two.setPixelColor(i, color)
                
        else:
            # Bei nicht-Regenbogen Farben
            # Links: Original-Farbe mit variabler Intensität
            for i in range(Config.LED_PER_STRIP):
                if i < left_leds:
                    # Intensität basierend auf Position
                    scale = max(0.1, (0.5 + 0.5 * i / Config.LED_PER_STRIP) * (left_amplitude / 100.0))
                    r = min(255, int(((base_color >> 16) & 0xFF) * scale))
                    g = min(255, int(((base_color >> 8) & 0xFF) * scale))
                    b = min(255, int((base_color & 0xFF) * scale))
                    color = Color(r, g, b)
                else:
                    color = Color(0, 0, 0)  # Aus
                self.strip_one.setPixelColor(i, color)
            
            # Rechts: Komplementärfarbe für Kontrast
            complement_r = 255 - ((base_color >> 16) & 0xFF)
            complement_g = 255 - ((base_color >> 8) & 0xFF)
            complement_b = 255 - (base_color & 0xFF)
            
            for i in range(Config.LED_PER_STRIP):
                if i < right_leds:
                    # Intensität basierend auf Position
                    scale = max(0.1, (0.5 + 0.5 * i / Config.LED_PER_STRIP) * (right_amplitude / 100.0))
                    r = min(255, int(complement_r * scale))
                    g = min(255, int(complement_g * scale))
                    b = min(255, int(complement_b * scale))
                    color = Color(r, g, b)
                else:
                    color = Color(0, 0, 0)  # Aus
                self.strip_two.setPixelColor(i, color)
        
        # Aktualisiere die Strips
        self.strip_one.show()
        self.strip_two.show()



    def _visualize_stereo_pulse(self):
        """
        Visualisiert die Audioamplitude als pulsierender Stereo-Effekt.
        Jeder LED-Strip pulst individuell mit der Musik des entsprechenden Kanals.
        Strip_one zeigt den linken Kanal, strip_two zeigt den rechten Kanal.
        """
        # Aktuelle Amplituden für linken und rechten Kanal
        left_amplitude = self.amplitude_smooth_left
        right_amplitude = self.amplitude_smooth_right
        
        # Helligkeit basierend auf Amplitude
        left_brightness = int((left_amplitude / 100.0) * 255)
        right_brightness = int((right_amplitude / 100.0) * 255)
        
        # Farbe basierend auf Config
        base_color = self._get_color_from_config()
        
        # Skalierungsfaktoren für RGB-Werte basierend auf Amplitude
        left_scale = max(0.1, left_amplitude / 100.0)
        right_scale = max(0.1, right_amplitude / 100.0)
        
        # Linker Kanal - alle LEDs im linken Strip pulsieren gleichmäßig
        for i in range(Config.LED_PER_STRIP):
            if Config.LED_COLOR.lower() == 'rainbow':
                # Rainbow-Effekt mit amplitudenabhängiger Helligkeit für linken Kanal
                # Farbverlauf von blau (niedrig) zu rot (hoch)
                hue = (i / float(Config.LED_PER_STRIP) + time.time() * 0.1) % 1.0
                # Modifiziere Farbton leicht für linken Kanal (kühler)
                hue = (hue + 0.7) % 1.0
                color = self._get_rainbow_color(hue, left_brightness)
            else:
                # Skaliere die Farbe basierend auf der Amplitude
                r = min(255, int(((base_color >> 16) & 0xFF) * left_scale))
                g = min(255, int(((base_color >> 8) & 0xFF) * left_scale))
                b = min(255, int((base_color & 0xFF) * left_scale))
                color = Color(r, g, b)
            
            self.strip_one.setPixelColor(i, color)
        
        # Rechter Kanal - alle LEDs im rechten Strip pulsieren gleichmäßig
        for i in range(Config.LED_PER_STRIP):
            if Config.LED_COLOR.lower() == 'rainbow':
                # Rainbow-Effekt mit amplitudenabhängiger Helligkeit für rechten Kanal
                # Farbverlauf von grün (niedrig) zu gelb (hoch)
                hue = (i / float(Config.LED_PER_STRIP) + time.time() * 0.1) % 1.0
                # Modifiziere Farbton leicht für rechten Kanal (wärmer)
                hue = (hue + 0.3) % 1.0
                color = self._get_rainbow_color(hue, right_brightness)
            else:
                # Bei nicht-Regenbogen Farben - Komplementärfarbe für rechten Kanal
                complement_r = 255 - ((base_color >> 16) & 0xFF)
                complement_g = 255 - ((base_color >> 8) & 0xFF)
                complement_b = 255 - (base_color & 0xFF)
                
                # Skaliere die Farbe basierend auf der Amplitude
                r = min(255, int(complement_r * right_scale))
                g = min(255, int(complement_g * right_scale))
                b = min(255, int(complement_b * right_scale))
                color = Color(r, g, b)
            
            self.strip_two.setPixelColor(i, color)
        
        # Aktualisiere die Strips
        self.strip_one.show()
        self.strip_two.show()


    def _visualize_stereo_center_bloom(self):
        """
        Stereo-Visualisierung: Symmetrisches Muster, das von der Mitte nach außen wächst.
        Jeder LED-Strip zeigt einen eigenen Kanal an.
        Strip_one zeigt den linken Kanal, strip_two zeigt den rechten Kanal.
        """
        # Aktuelle Amplituden für linken und rechten Kanal
        left_amplitude = self.amplitude_smooth_left
        right_amplitude = self.amplitude_smooth_right
        
        # Berechne, wie viele LEDs für jeden Kanal leuchten sollen (von der Mitte aus)
        center = Config.LED_PER_STRIP // 2
        left_radius = int((left_amplitude / 100.0) * (Config.LED_PER_STRIP // 2))
        right_radius = int((right_amplitude / 100.0) * (Config.LED_PER_STRIP // 2))
        
        # Setze alle LEDs zunächst auf aus
        for i in range(Config.LED_PER_STRIP):
            self.strip_one.setPixelColor(i, Color(0, 0, 0))
            self.strip_two.setPixelColor(i, Color(0, 0, 0))
        
        # Farbe basierend auf Config
        base_color = self._get_color_from_config()
        
        # Linker Kanal - strip_one
        for offset in range(left_radius + 1):
            # Berechne Position links und rechts vom Zentrum
            left = center - offset
            right = center + offset
            
            # Intensität basierend auf Entfernung vom Zentrum
            intensity = 255 - int(255 * (offset / (Config.LED_PER_STRIP / 2)))
            intensity = max(50, intensity)
            
            if Config.LED_COLOR.lower() == 'rainbow':
                # Zeit-basierte Farbänderung für pulsierenden Regenbogeneffekt
                # Modifiziere Farbton leicht für linken Kanal (kühler)
                hue = (offset / float(Config.LED_PER_STRIP) + time.time() * 0.2) % 1.0
                hue = (hue + 0.7) % 1.0  # Blau-Bereich
                color = self._get_rainbow_color(hue, intensity)
            else:
                # Skaliere die Farbe basierend auf der Intensität
                r = min(255, int(((base_color >> 16) & 0xFF) * intensity / 255))
                g = min(255, int(((base_color >> 8) & 0xFF) * intensity / 255))
                b = min(255, int((base_color & 0xFF) * intensity / 255))
                color = Color(r, g, b)
            
            # Setze die Farben links und rechts vom Zentrum für linken Kanal
            if 0 <= left < Config.LED_PER_STRIP:
                self.strip_one.setPixelColor(left, color)
            
            if 0 <= right < Config.LED_PER_STRIP and right != left:
                self.strip_one.setPixelColor(right, color)
        
        # Rechter Kanal - strip_two
        for offset in range(right_radius + 1):
            # Berechne Position links und rechts vom Zentrum
            left = center - offset
            right = center + offset
            
            # Intensität basierend auf Entfernung vom Zentrum
            intensity = 255 - int(255 * (offset / (Config.LED_PER_STRIP / 2)))
            intensity = max(50, intensity)
            
            if Config.LED_COLOR.lower() == 'rainbow':
                # Zeit-basierte Farbänderung für pulsierenden Regenbogeneffekt
                # Modifiziere Farbton leicht für rechten Kanal (wärmer)
                hue = (offset / float(Config.LED_PER_STRIP) + time.time() * 0.2) % 1.0
                hue = (hue + 0.3) % 1.0  # Grün-Gelb-Bereich
                color = self._get_rainbow_color(hue, intensity)
            else:
                # Bei nicht-Regenbogen Farben - Komplementärfarbe für rechten Kanal
                complement_r = 255 - ((base_color >> 16) & 0xFF)
                complement_g = 255 - ((base_color >> 8) & 0xFF)
                complement_b = 255 - (base_color & 0xFF)
                
                # Skaliere die Farbe basierend auf der Intensität
                r = min(255, int(complement_r * intensity / 255))
                g = min(255, int(complement_g * intensity / 255))
                b = min(255, int(complement_b * intensity / 255))
                color = Color(r, g, b)
            
            # Setze die Farben links und rechts vom Zentrum für rechten Kanal
            if 0 <= left < Config.LED_PER_STRIP:
                self.strip_two.setPixelColor(left, color)
            
            if 0 <= right < Config.LED_PER_STRIP and right != left:
                self.strip_two.setPixelColor(right, color)
        
        # Aktualisiere die Strips
        self.strip_one.show()
        self.strip_two.show()