import socket
import subprocess

# Konfigurationseinstellungen für LED-Visualisierung
class Config:   
    # LED-Konfiguration
    LED_PER_STRIP = 20                   # Anzahl LED pro Srtip       
    LED_PIN_ONE = 18                     # GPIO Pin für erster Streinfen 
    LED_PIN_TWO = 13                     # GPIO Pin für zweiter Streinfen
    LED_FREQ_HZ = 800000                 # Signalfrequenz für die LED-Kommunikation (800kHz)
    LED_DMA_ONE = 10                     # DMA-Kanäle (Direct Memory Access) für die LED-Steuerung
    LED_DMA_TWO = 11                     # Separater Kanal
    LED_BRIGHTNESS = 50                  # Helligkeit 50%
    LED_INVERT = False                   # 
    LED_CHANNEL_ONE = 0                  # PWM-Kanäle für die LED-Steuerung 
    LED_CHANNEL_TWO = 1                  # Separate Kanäle für die zwei LED-Streifen 
    # Audio-Visualisierungs-Einstellungen
    AUDIO_SMOOTHING = 0.3                 # Glättungsfaktor für Audio-Visualisierung (0.3)
    AUDIO_FORMAT = 'int16'                # Audioformat für die Aufnahme (16-bit Integer)     
    AUDIO_CHANNELS = 1                    # Anzahl der Audiokanäle (Mono-Aufnahme)  
    AUDIO_RATE = 44100                    # Audio-Abtastrate (44.1kHz, CD-Qualität)  
    AUDIO_CHUNK = 1024                    #   Größe der Audio-Chunks für die Verarbeitung
                                        # Kleinere Werte erhöhen die Reaktionsgeschwindigkeit, erhöhen aber auch CPU-Last
    # Muster-Visualisierungs-Einstellungen
    VISUALIZATION_MODE = 'audio'        # Standardmodus = audio, static, off
    AUDIO_PATTERN = 'audio_pattern_01'   # LED Modus wenn Audiosynchronsierung ausgewählt ist
    STATIC_PATTERN = 'static_pattern_01' # LED Modus wenn KEINE Audiosynchronsierung ausgewählt ist

    LED_COLOR = 'rainbow'                      # hier werden namen verwendet z. B. GREEN = nur Grün, RAINBOW = verschiedene REGENB Bogen Farben

    
    @classmethod
    def set_visualization_mode(cls, mode):
        """
        Ändert den Visualisierungsmodus
        
        :param mode: Einer der unterstützten Modi ('audio', 'static', 'off')
        """
        if mode in ['audio', 'static', 'off']:
            cls.VISUALIZATION_MODE = mode
        else:
            raise ValueError(f"Ungültiger Visualisierungsmodus: {mode}")
    
    @classmethod
    def set_pattern_per_mode(cls, pattern):
        # Prüfen, welcher Modus aktiv ist und entsprechend das Muster setzen
        if cls.VISUALIZATION_MODE == 'audio':
            if pattern in ['audio_pattern_01', 'audio_pattern_02', 'audio_pattern_03','audio_pattern_04','audio_pattern_05','audio_pattern_06']:
                cls.AUDIO_PATTERN = pattern
            else:
                raise ValueError(f"Ungültiges Audio-Muster: {pattern}")
        elif cls.VISUALIZATION_MODE == 'static':
            if pattern in ['static_pattern_01', 'static_pattern_02', 'static_pattern_03', 'static_pattern_04']:
                cls.STATIC_PATTERN = pattern
            else:
                raise ValueError(f"Ungültiges Static-Muster: {pattern}")
        elif cls.VISUALIZATION_MODE == 'off':
            # Im Off-Modus gibt es keine Muster zum Setzen
            pass
        else:
            raise ValueError(f"Ungültiger Visualisierungsmodus: {cls.VISUALIZATION_MODE}")
    
    @classmethod
    def get_ip_addresses(cls):
        """
        Ermittelt alle IP-Adressen des Geräts (speziell für Raspberry Pi)
        
        :return: Liste mit IP-Adressen
        """
        ip_addresses = []
        
        try:
            # Methode 1: Direkter Zugriff über Socket-Verbindung
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # Verbindung zu einem externen Server (hier Google DNS)
            # Wir müssen keine echte Verbindung herstellen, nur die Route
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            ip_addresses.append(f"IP: {ip}")
            
            # Methode 2: Hostname
            hostname = socket.gethostname()
            ip_addresses.append(f"Hostname: {hostname}")
            
            # Methode 3: Befehl auf Raspberry Pi ausführen (funktioniert nur auf Linux)
            try:
                cmd = "hostname -I"
                result = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
                ips = result.split()
                for ip in ips:
                    if ip and ip not in [entry.split(': ')[1] for entry in ip_addresses if ': ' in entry]:
                        ip_addresses.append(f"IP: {ip}")
            except Exception as e:
                # Falls Befehl fehlschlägt, ignorieren
                pass
                
        except Exception as e:
            # Bei Fehlern eine Meldung hinzufügen
            ip_addresses.append(f"IP-Fehler: {str(e)}")
        
        return ip_addresses

    @classmethod
    def to_json(cls):
        """
        Konvertiert die aktuelle Konfiguration in ein JSON-kompatibles Dictionary.
        Dies ermöglicht es, die vollständige Konfiguration an den Client zu senden.
        
        Returns:
            dict: Ein Dictionary mit allen relevanten Konfigurationsparametern
        """
        # Hole passenden Pattern-Namen basierend auf dem aktiven Modus
        pattern_name = ""
        pattern_id = ""
        
        if cls.VISUALIZATION_MODE == 'audio':
            pattern_id = cls.AUDIO_PATTERN
            if pattern_id == 'audio_pattern_01':
                pattern_name = "Spektrum"
            elif pattern_id == 'audio_pattern_02':
                pattern_name = "Equalizer"
            elif pattern_id == 'audio_pattern_03':
                pattern_name = "Beat"
            elif pattern_id == 'audio_pattern_04':
                pattern_name = "Stereo 01"
        elif cls.VISUALIZATION_MODE == 'static':
            pattern_id = cls.STATIC_PATTERN
            if pattern_id == 'static_pattern_01':
                pattern_name = "Simple Pulse"
            elif pattern_id == 'static_pattern_02':
                pattern_name = "Ping Pong"
            elif pattern_id == 'static_pattern_03':
                pattern_name = "Dual Puls"
            elif pattern_id == 'static_pattern_04':
                pattern_name = "Matrix"
        else:
            pattern_name = "Aus"
        
        # Hole den Farbnamen in benutzerfreundlichem Format
        color_name = ""
        if cls.LED_COLOR.lower() == 'rainbow':
            color_name = "Regenbogen"
        elif cls.LED_COLOR.lower() == 'green':
            color_name = "Grün"
        elif cls.LED_COLOR.lower() == 'blue':
            color_name = "Blau"
        elif cls.LED_COLOR.lower() == 'red':
            color_name = "Rot"
        elif cls.LED_COLOR.lower() == 'purple':
            color_name = "Lila"
        elif cls.LED_COLOR.lower() == 'yellow':
            color_name = "Gelb"
        else:
            color_name = cls.LED_COLOR
        
        # Modus-Name in benutzerfreundlichem Format
        mode_name = ""
        if cls.VISUALIZATION_MODE == 'audio':
            mode_name = "Audio"
        elif cls.VISUALIZATION_MODE == 'static':
            mode_name = "Statisch"
        else:
            mode_name = "Aus"
        
        # Erstelle das Config-Dictionary
        config_dict = {
            # Technische Werte (für die Logik)
            "visualization_mode": cls.VISUALIZATION_MODE,
            "audio_pattern": cls.AUDIO_PATTERN,
            "static_pattern": cls.STATIC_PATTERN,
            "current_pattern": pattern_id,
            "led_color": cls.LED_COLOR.lower(),
            "led_brightness": cls.LED_BRIGHTNESS,
            
            # Benutzerfreundliche Werte (für die Anzeige)
            "display": {
                "mode_name": mode_name,
                "color_name": color_name,
                "pattern_name": pattern_name,
                "ip_addresses": cls.get_ip_addresses()
            }
        }
        
        return config_dict