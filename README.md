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

5. Kontrolle der Audio Schnitstelle
```bash 
cat /proc/asound/modules

sudo nano /etc/modprobe.d/alsa-base.conf
```

6. Füge folgende Zeilen in den Editor und starte den Pi danach neu.
```bash 
options snd_usb_audio index=0
options snd_bcm2835 index=1
options snd slots=snd-usb-audio,snd-bcm2835
```

7. Nach dem Neustart sollte die Ausgabe nun die snd_bcm2835 als 0 definiert haben.
```bash 
cat /proc/asound/modules
```

8. Weitere installiert pakete
sudo apt-get install libopenblas-dev
sudo apt-get install portaudio19-dev
pip uninstall numpy
pip install numpy
sudo nano /etc/asound.conf
pcm.!default {
    type asym
    playback.pcm "hw:0,0"
    capture.pcm "dsnoop"
}

pcm.dummy {
    type null
    slave.pcm "hw:0,0"
}

pcm.dsnoop {
    type dmix
    ipc_key 1234
    slave {
        pcm "dummy"
        period_time 0
        period_size 1024
        buffer_size 4096
        rate 44100
        channels 2
    }
}

nano /etc/modprobe.d/raspi-blacklist.conf 
blacklist snd_bcm2835

sudo nano /boot/firmware/config.txt
# I2S Mikrofon Aktivierung
dtoverlay=i2s-mems-mic

# ALSA für Recording aktivieren
dtparam=audio=on

# Enable audio (loads snd_bcm2835)
dtparam=audio=off


sudo apt-get install alsa-utils

jetzt richtig?
sudo nano /etc/asound.conf
reboot pi


und jetzt?
cat <<EOF | sudo tee /etc/modprobe.d/blacklist-rgb-matrix.conf
blacklist snd_bcm2835
EOF

sudo update-initramfs -u

# Verkabelung
Gemäss Bild Pi-Ping-Belegung

# Start des Projekte
Die App kann nur als root gestartet werden also:
1. sudo su
2. source venv/bin/activate
3. python3 main.py