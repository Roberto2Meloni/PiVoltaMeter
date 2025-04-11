# Konfigurationseinstellungen für LED-Visualisierung

class Config:
    # Visualisierungsmodus
    VISUALIZATION_MODE = 'audio'  # Mögliche Werte: 'audio', 'pattern', 'static'
    
    # LED-Konfiguration
    LED_PER_STRIP = 10
    LED_PIN = 18
    LED_PIN_TWO = 13
    LED_FREQ_HZ = 800000
    LED_DMA = 10
    LED_DMA_TWO = 11
    LED_BRIGHTNESS = 50
    LED_INVERT = False
    LED_CHANNEL_ONE = 0
    LED_CHANNEL_TWO = 1

    # Audio-Visualisierungs-Einstellungen
    AUDIO_SMOOTHING = 0.3
    AUDIO_FORMAT = 'int16'
    AUDIO_CHANNELS = 1
    AUDIO_RATE = 44100
    AUDIO_CHUNK = 1024

    # Muster-Visualisierungs-Einstellungen
    DEFAULT_PATTERN = 'rainbow'  # Standardmuster
    VISUALIZATION_MODE = 'static'  # Standardmodus

    @classmethod
    def set_visualization_mode(cls, mode):
        """
        Ändert den Visualisierungsmodus
        
        :param mode: Einer der unterstützten Modi ('audio', 'pattern', 'static')
        """
        if mode in ['audio', 'pattern', 'static']:
            cls.VISUALIZATION_MODE = mode
        else:
            raise ValueError(f"Ungültiger Visualisierungsmodus: {mode}")