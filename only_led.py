
import time
import random
from rpi_ws281x import PixelStrip, Color
import pyaudio
import numpy as np

# Konfiguration für die WS2812b LEDs
LED_PER_STRIP = 10
LED_PIN = 18          # GPIO-Pin (18 = PWM0)
LED_PIN_TWO = 13      # GPIO-Pin für zweiten Strip (13 = PWM1)
LED_FREQ_HZ = 800000  # LED-Signalfrequenz
LED_DMA = 10          # DMA-Kanal für ersten Strip
LED_DMA_TWO = 11      # DMA-Kanal für zweiten Strip
LED_BRIGHTNESS = 50   # Helligkeit (0-255)
LED_INVERT = False    # Signal invertieren
LED_CHANNEL_ONE = 0   # PWM-Kanal für Strip 1 (0 für GPIO 18)
LED_CHANNEL_TWO = 1   # PWM-Kanal für Strip 2 (1 für GPIO 13)
LED_STRIP_ONE_MAX_COUNT = LED_PER_STRIP  # Maximale Anzahl der LEDs in der Start-Animation
LED_STRIP_TWO_MAX_COUNT = LED_PER_STRIP  # Maximale Anzahl der LEDs in der Start-Animation



# Initialisierung der LED-Streifen
strip_one = PixelStrip(LED_STRIP_ONE_MAX_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL_ONE)
strip_two = PixelStrip(LED_STRIP_TWO_MAX_COUNT, LED_PIN_TWO, LED_FREQ_HZ, LED_DMA_TWO, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL_TWO)
strip_one.begin()
strip_two.begin()  # Strip zwei starten

def random_color():
    """Erzeugt eine zufällige RGB-Farbe"""
    return Color(
        random.randint(0, 255),  # R
        random.randint(0, 255),  # G
        random.randint(0, 255)   # B
    )



def start_phase_one():
    """Start-Animation: LEDs werden nacheinander mit zufälligen Farben eingeschaltet"""
    print("Starte die Einschaltsequenz 1...")
    
    # Zuerst alle LEDs ausschalten
    for i in range(LED_PER_STRIP):
        strip_one.setPixelColor(i, Color(0, 0, 0))
        strip_two.setPixelColor(i, Color(0, 0, 0))
    strip_one.show()
    strip_two.show()
    
    
    # Schalte LEDs nacheinander ein
    for i in range(LED_STRIP_ONE_MAX_COUNT):
        # Setze eine zufällige Farbe für diese LED
        strip_one.setPixelColor(i, random_color())
        strip_two.setPixelColor(i, random_color())
        
        # Aktualisiere die LED-Anzeige
        strip_one.show()
        strip_two.show()
        
        # Warte 0.1 Sekunden vor der nächsten LED
        time.sleep(0.1)
    
    print(f"{LED_PER_STRIP} LEDs wurden aktiviert.")


    
    # Dann schalten wir sie aus
    print("Schalte alle LEDs aus...")
    for i in range(LED_PER_STRIP ):
        strip_one.setPixelColor(i, Color(0, 0, 0))
        strip_two.setPixelColor(i, Color(0, 0, 0))
        strip_one.show()  # Diese Zeile muss innerhalb der Schleife sein
        strip_two.show()  # Diese Zeile muss innerhalb der Schleife sein
        time.sleep(0.1)   # Verzögerung für den Animationseffekt


def start_phase_two():
    """Start-Animation: LEDs werden nacheinander mit zufälligen Farben eingeschaltet"""
    print("Starte die Einschaltsequenz 2...")
    
    # Zuerst alle LEDs ausschalten
    for i in range(LED_STRIP_ONE_MAX_COUNT):
        strip_one.setPixelColor(i, Color(0, 0, 0))
        strip_two.setPixelColor(i, Color(0, 0, 0))
    strip_one.show()
    strip_two.show()
    
    
    # Schalte LEDs nacheinander ein
    for i in range(LED_PER_STRIP - 1, -1, -1):
        # Setze eine zufällige Farbe für diese LED
        strip_one.setPixelColor(i, random_color())
        strip_two.setPixelColor(i, random_color())
        
        # Aktualisiere die LED-Anzeige
        strip_one.show()
        strip_two.show()
        
        # Warte 0.1 Sekunden vor der nächsten LED
        time.sleep(0.1)
    
    print(f"{LED_PER_STRIP} LEDs wurden aktiviert.")


    
    # Dann schalten wir sie nacheinander rückwärts aus
    print("Schalte LEDs rückwärts nacheinander aus...")
    for i in range(LED_PER_STRIP - 1, -1, -1):
        strip_one.setPixelColor(i, Color(0, 0, 0))
        strip_two.setPixelColor(i, Color(0, 0, 0))
        strip_one.show()  # Diese Zeile muss innerhalb der Schleife sein
        strip_two.show()  # Diese Zeile muss innerhalb der Schleife sein
        time.sleep(0.1)   # Verzögerung für den Animationseffekt

def start_phase_three():
    """
    Start-Animation: 
    - Alle LEDs werden für 0.5s rot
    - Alle LEDs werden für 0.5s gelb
    - Alle LEDs werden für 0.5s grün
    - Alle LEDs werden ausgeschaltet
    """
    print("Starte die Einschaltsequenz 3...")
    
    # Rot - alle LEDs auf einmal
    print("Alle LEDs rot...")
    for i in range(LED_PER_STRIP):
        strip_one.setPixelColor(i, Color(255, 0, 0))  # Rot
        strip_two.setPixelColor(i, Color(255, 0, 0))  # Rot
    strip_one.show()
    strip_two.show()
    time.sleep(0.5)  # 0.5 Sekunden warten
    
    # Gelb - alle LEDs auf einmal
    print("Alle LEDs gelb...")
    for i in range(LED_PER_STRIP):
        strip_one.setPixelColor(i, Color(255, 255, 0))  # Gelb
        strip_two.setPixelColor(i, Color(255, 255, 0))  # Gelb
    strip_one.show()
    strip_two.show()
    time.sleep(0.5)  # 0.5 Sekunden warten
    
    # Grün - alle LEDs auf einmal
    print("Alle LEDs grün...")
    for i in range(LED_PER_STRIP):
        strip_one.setPixelColor(i, Color(0, 255, 0))  # Grün
        strip_two.setPixelColor(i, Color(0, 255, 0))  # Grün
    strip_one.show()
    strip_two.show()
    time.sleep(0.5)  # 0.5 Sekunden warten
    
    # Alle LEDs ausschalten
    print("Alle LEDs aus...")
    for i in range(LED_PER_STRIP):
        strip_one.setPixelColor(i, Color(0, 0, 0))  # Aus
        strip_two.setPixelColor(i, Color(0, 0, 0))  # Aus
    strip_one.show()
    strip_two.show()
    
    print("Ampel-Sequenz abgeschlossen.")

def start_all_start_phase():
    start_phase_one()
    # start_phase_two()
    # start_phase_three()


def animation_webserver_starting(iterations=1):
    """
    Animation beim Starten des Webservers - blaues sequentielles Ein- und Ausschalten
    iterations: Anzahl der Durchläufe (Standard: 1, für Endlosschleife -1 verwenden)
    """
    print("Webserver wird gestartet - Animation läuft...")
    
    count = 0
    while iterations == -1 or count < iterations:
        count += 1
        
        # Alle LEDs ausschalten
        for i in range(LED_PER_STRIP):
            strip_one.setPixelColor(i, Color(0, 0, 0))
            strip_two.setPixelColor(i, Color(0, 0, 0))
        strip_one.show()
        strip_two.show()
        
        # Blaues Licht sequentiell einschalten (von LED 1 bis zur letzten)
        for i in range(LED_PER_STRIP):
            # Setze aktuelle LED auf Blau
            strip_one.setPixelColor(i, Color(0, 0, 255))  # Blau
            strip_two.setPixelColor(i, Color(0, 0, 255))  # Blau
            
            # Aktualisiere die LED-Anzeige
            strip_one.show()
            strip_two.show()
            
            # Kurze Pause
            time.sleep(0.1)
        
        # Kurze Pause, wenn alle LEDs eingeschaltet sind
        time.sleep(0.3)
        
        # Blaues Licht sequentiell ausschalten (von LED 1 bis zur letzten)
        for i in range(LED_PER_STRIP):
            # Setze aktuelle LED aus
            strip_one.setPixelColor(i, Color(0, 0, 0))  # Aus
            strip_two.setPixelColor(i, Color(0, 0, 0))  # Aus
            
            # Aktualisiere die LED-Anzeige
            strip_one.show()
            strip_two.show()
            
            # Kurze Pause
            time.sleep(0.1)


def animation_webserver_ready():
    """Animation wenn der Webserver bereit ist - grünes Aufleuchten"""
    print("Webserver ist bereit - Animation läuft...")
    
    # Alle LEDs grün
    for i in range(LED_PER_STRIP):
        strip_one.setPixelColor(i, Color(0, 255, 0))  # Grün
        strip_two.setPixelColor(i, Color(0, 255, 0))  # Grün
    strip_one.show()
    strip_two.show()
    time.sleep(1)
    
    # Langsam ausblenden
    for brightness in range(100, 0, -5):
        for i in range(LED_PER_STRIP):
            green_value = int(brightness * 2.55)
            strip_one.setPixelColor(i, Color(0, green_value, 0))
            strip_two.setPixelColor(i, Color(0, green_value, 0))
        strip_one.show()
        strip_two.show()
        time.sleep(0.05)

def animation_webserver_error(loop=True):
    """Animation wenn der Webserver nicht gestartet werden konnte - rotes Blinken"""
    print("Webserver-Fehler - Animation läuft...")
    
    # Anzahl der Durchläufe
    cycles = 1000 if loop else 5  # Wenn loop=True, dann quasi endlos, sonst 5 Zyklen
    
    for _ in range(cycles):
        # Alle LEDs rot
        for i in range(LED_PER_STRIP):
            strip_one.setPixelColor(i, Color(255, 0, 0))  # Rot
            strip_two.setPixelColor(i, Color(255, 0, 0))  # Rot
        strip_one.show()
        strip_two.show()
        time.sleep(0.5)
        
        # Alle LEDs aus
        for i in range(LED_PER_STRIP):
            strip_one.setPixelColor(i, Color(0, 0, 0))  # Aus
            strip_two.setPixelColor(i, Color(0, 0, 0))  # Aus
        strip_one.show()
        strip_two.show()
        time.sleep(0.5)

def pulsing_all_led(color_hex, cycles=3):
    """
    Lässt alle LEDs in der angegebenen Farbe pulsieren
    
    Parameter:
    color_hex (str): Hexadezimaler Farbwert (z.B. "#FF0000" für Rot)
    cycles (int): Anzahl der Pulsier-Zyklen
    """
    print(f"Pulsieren in Farbe {color_hex}...")
    
    # Hexwert in RGB-Komponenten umwandeln
    color_hex = color_hex.lstrip('#')
    r = int(color_hex[0:2], 16)
    g = int(color_hex[2:4], 16)
    b = int(color_hex[4:6], 16)
    
    # Mehrere Pulsier-Zyklen durchführen
    for _ in range(cycles):
        # Helligkeit erhöhen (0% bis 100%)
        for brightness in range(0, 101, 2):
            brightness_factor = brightness / 100.0
            
            # Aktuelle Farbwerte berechnen
            current_r = int(r * brightness_factor)
            current_g = int(g * brightness_factor)
            current_b = int(b * brightness_factor)
            
            # Alle LEDs auf aktuelle Farbe setzen
            for i in range(LED_PER_STRIP):
                strip_one.setPixelColor(i, Color(current_r, current_g, current_b))
                strip_two.setPixelColor(i, Color(current_r, current_g, current_b))
            
            # LED-Streifen aktualisieren
            strip_one.show()
            strip_two.show()
            
            # Kurze Pause
            time.sleep(0.01)
        
        # Kurze Pause bei voller Helligkeit
        time.sleep(0.2)
        
        # Helligkeit verringern (100% bis 0%)
        for brightness in range(100, -1, -2):
            brightness_factor = brightness / 100.0
            
            # Aktuelle Farbwerte berechnen
            current_r = int(r * brightness_factor)
            current_g = int(g * brightness_factor)
            current_b = int(b * brightness_factor)
            
            # Alle LEDs auf aktuelle Farbe setzen
            for i in range(LED_PER_STRIP):
                strip_one.setPixelColor(i, Color(current_r, current_g, current_b))
                strip_two.setPixelColor(i, Color(current_r, current_g, current_b))
            
            # LED-Streifen aktualisieren
            strip_one.show()
            strip_two.show()
            
            # Kurze Pause
            time.sleep(0.01)
        
        # Kurze Pause bei 0% Helligkeit
        time.sleep(0.2)
    
    # Alle LEDs ausschalten
    for i in range(LED_PER_STRIP):
        strip_one.setPixelColor(i, Color(0, 0, 0))
        strip_two.setPixelColor(i, Color(0, 0, 0))
    strip_one.show()
    strip_two.show()

def hsv_to_rgb(h, s, v):
    """Konvertiert HSV-Farbwerte in RGB"""
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

def audio_visualizer():
    # Audio-Parameter
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    
    # Verwende einen Glättungsfaktor für flüssigere Übergänge
    smoothing = 0.3  # Niedrigerer Wert = weniger Glättung, höherer Wert = mehr Glättung
    last_amplitude = 0
    
    p = pyaudio.PyAudio()
    
    # Geräteinformationen ausgeben
    print("Verfügbare Audiogeräte:")
    for i in range(p.get_device_count()):
        dev_info = p.get_device_info_by_index(i)
        print(f"Device {i}: {dev_info['name']}")
        print(f"  Max Input Channels: {dev_info['maxInputChannels']}")
        print(f"  Default Sample Rate: {dev_info['defaultSampleRate']}")
    
    # Finde das erste Eingabegerät
    device_index = None
    for i in range(p.get_device_count()):
        dev_info = p.get_device_info_by_index(i)
        if dev_info['maxInputChannels'] > 0:
            device_index = i
            break
    
    if device_index is None:
        print("Kein Eingabegerät gefunden!")
        return
    
    try:
        print(f"Öffne Audiogerät {device_index}...")
        stream = p.open(format=FORMAT,
                       channels=CHANNELS,
                       rate=RATE,
                       input=True,
                       input_device_index=device_index,
                       frames_per_buffer=CHUNK)
        
        print("Audio-Visualisierung gestartet... (Drücken Sie Strg+C zum Beenden)")
        
        while True:
            # Lese Audiodaten
            data = stream.read(CHUNK, exception_on_overflow=False)
            
            # Konvertiere zu numpy array
            audio_data = np.frombuffer(data, dtype=np.int16)
            
            # Sichere Berechnung der RMS-Amplitude
            if len(audio_data) > 0 and np.any(np.isfinite(audio_data)):
                # Berechne RMS-Amplitude
                amplitude_rms = np.sqrt(np.mean(np.square(audio_data.astype(float))))
                
                # Normalisiere auf Bereich 0-100
                amplitude_scaled = min(100, int(amplitude_rms / 32768 * 100))
                
                # Wende Glättung an
                smoothed_amplitude = last_amplitude * smoothing + amplitude_scaled * (1 - smoothing)
                last_amplitude = smoothed_amplitude
                
                # Visualisiere in Konsole
                bar = '#' * int(smoothed_amplitude / 2)
                print(f"Amplitude: {smoothed_amplitude:3.1f}/100 |{bar:<50}|", end='\r')
                
                # Berechne, wie viele LEDs leuchten sollen
                num_leds = int(smoothed_amplitude / 100 * LED_PER_STRIP)
                
                # Aktualisiere LEDs
                for i in range(LED_PER_STRIP):
                    if i < num_leds:
                        # Farbverlauf von Grün zu Rot
                        hue = (120 - (i * 120 / LED_PER_STRIP)) / 360.0
                        r, g, b = [int(x * 255) for x in hsv_to_rgb(hue, 1.0, 1.0)]
                        strip_one.setPixelColor(i, Color(r, g, b))
                        strip_two.setPixelColor(i, Color(r, g, b))
                    else:
                        strip_one.setPixelColor(i, Color(0, 0, 0))
                        strip_two.setPixelColor(i, Color(0, 0, 0))
                
                strip_one.show()
                strip_two.show()
            else:
                print("Keine gültigen Audiodaten gefunden.", end='\r')
    
    except KeyboardInterrupt:
        print("\nBeendet.")
    except Exception as e:
        print(f"\nFehler: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if 'stream' in locals():
            stream.stop_stream()
            stream.close()
        p.terminate()
        
        # Alle LEDs ausschalten
        for i in range(LED_PER_STRIP):
            strip_one.setPixelColor(i, Color(0, 0, 0))
            strip_two.setPixelColor(i, Color(0, 0, 0))
        strip_one.show()
        strip_two.show()