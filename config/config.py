# Konfigurationseinstellungen für LED-Visualisierung

class Config:   
    # LED-Konfiguration
    LED_PER_STRIP = 10                   # Anzahl LED pro Srtip       
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
    DEFAULT_PATTERN = 'rainbow'         # Standardmuster
    VISUALIZATION_MODE = 'audio'        # Standardmodus = audio, pattern, Static


    # Neue Konfigurationsoption für Amplituden-Farbe
    AMPLITUDE_COLOR_MODE = 'fixed'    # Mögliche Werte: 'dynamic', 'fixed'
    FIXED_AMPLITUDE_COLOR = '#00FF00'   # Standardfarbe Grün

    @classmethod
    def set_visualization_mode(cls, mode):
        """
        Ändert den Visualisierungsmodus
        
        :param mode: Einer der unterstützten Modi ('audio', 'pattern', 'off')
        """
        if mode in ['audio', 'pattern', 'off']:
            cls.VISUALIZATION_MODE = mode
        else:
            raise ValueError(f"Ungültiger Visualisierungsmodus: {mode}")

    # @classmethod
    # def set_amplitude_color(cls, color):
    #     """
    #     Setzt die Farbe für die Amplituden-Visualisierung
        
    #     :param color: Hex-Farbwert
    #     """
    #     cls.FIXED_AMPLITUDE_COLOR = color
    #     cls.AMPLITUDE_COLOR_MODE = 'fixed'