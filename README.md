# PiVoltMeter

![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-C51A4A?style=for-the-badge&logo=Raspberry-Pi)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)

Ein interaktives LED-Steuerungssystem für den Raspberry Pi, das WS2812b LED-Streifen über eine Weboberfläche kontrolliert.

## 🚀 Features

- Steuerung von zwei WS2812b LED-Streifen (PWM-Pins 18 und 13)
- Webbasierte Benutzeroberfläche
- Verschiedene LED-Animationen und -Sequenzen
- Farbauswahl und -steuerung
- Pulsierende Farbeffekte mit einstellbarer Zyklenanzahl

## 📋 Voraussetzungen

- Raspberry Pi (getestet auf Raspberry Pi 4)
- Python 3.7 oder höher
- WS2812b LED-Streifen
- 5V Stromversorgung für die LED-Streifen
- Internetbrowser für den Zugriff auf die Weboberfläche

## 🔧 Installation

1. Repository klonen:
```bash
git clone https://github.com/Roberto2Meloni/PiVoltaMeter.git
cd PiVoltMeter
```

2. Virtuelle Umgebung erstellen und aktivieren
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Abhängigkeiten installieren
```bash
pip install -r requirements.txt
```

4. Start der Applikation
```bash 
sudo python main.py
```