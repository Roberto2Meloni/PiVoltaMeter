# Datum:        08.04.2025
# Version:      1.0
# Beschreibung: Steuerung von WS2812b LEDs mit einem Raspberry Pi
# Releas Notes
# Version               Notes
# 1.0                   Erste Implementierung


from only_flask import start_flask_server

def main():
    """Hauptfunktion des Programms"""
    print("Start die Main funktion")
    
    # Führe die Start-Animation durch
    from only_led import start_all_start_phase
    start_all_start_phase()

    from only_flask import start_flask_server
    start_flask_server()


if __name__ == "__main__":
    main()