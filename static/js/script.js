console.log("Script wurde geladen");

// Visualisierungsmodus einstellen
function setVisualizationMode(mode, url) {
    // Entferne aktiven Status von allen Modus-Buttons
    document.querySelectorAll('#audio-mode, #pattern-mode, #off-mode').forEach(btn => {
        btn.classList.remove('active');
    });

    // Füge aktiven Status zum ausgewählten Button hinzu
    document.getElementById(mode + '-mode').classList.add('active');

    // Aktualisiere Status-Anzeige
    const modeText = mode === 'audio' ? 'Audio' : mode === 'pattern' ? 'Pattern' : 'Aus';
    document.getElementById('current-mode').textContent = modeText;

    // Mustergruppen anzeigen/verstecken basierend auf Modus
    document.querySelectorAll('.pattern-group').forEach(group => {
        group.style.display = 'none';
    });

    if (mode === 'off') {
        document.getElementById('off-info').style.display = 'block';
    } else {
        document.getElementById(mode + '-patterns').style.display = 'block';
        
        // Setze ersten Pattern-Button als aktiv, wenn Modus wechselt
        const patternButtons = document.querySelectorAll('#' + mode + '-patterns .pattern-btn');
        if (patternButtons.length > 0) {
            patternButtons.forEach(btn => btn.classList.remove('active'));
            patternButtons[0].classList.add('active');
        }
    }

    // Statusmeldung aktualisieren
    document.getElementById('status').innerHTML = '<i class="fas fa-info-circle"></i> Modus auf ' + modeText + ' gesetzt';

    // Optional: Sende Anfrage an Backend, um den Modus zu ändern
    if (url) {
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ mode: mode })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('Modus erfolgreich geändert');
            } else {
                console.error('Fehler beim Ändern des Modus:', data.message);
                document.getElementById('status').innerHTML = '<i class="fas fa-exclamation-triangle"></i> Fehler: ' + data.message;
            }
        })
        .catch(error => {
            console.error('Netzwerkfehler:', error);
            document.getElementById('status').innerHTML = '<i class="fas fa-exclamation-triangle"></i> Netzwerkfehler beim Ändern des Modus';
        });
    }
}

// Muster einstellen
function setPattern(patternId) {
    // Aktiven Status von allen Muster-Buttons im aktuellen Modus entfernen
    const activeMode = document.querySelector('#audio-mode, #pattern-mode, #off-mode.active').id.replace('-mode', '');
    
    if (activeMode !== 'off') {
        document.querySelectorAll('#' + activeMode + '-patterns .pattern-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        
        // Aktiven Status zum ausgewählten Muster hinzufügen
        document.getElementById(patternId).classList.add('active');
        
        // Hole den Musternamen für die Statusanzeige
        const patternName = document.getElementById(patternId).textContent.trim();
        
        // Statusmeldung aktualisieren
        document.getElementById('status').innerHTML = '<i class="fas fa-info-circle"></i> Muster auf ' + patternName + ' gesetzt';
        
        // Optional: Sende Anfrage an Backend
        // Diese Zeile kannst du nach deinen Bedürfnissen anpassen
        // fetch('/set_pattern', { ... })
    }
}

// Initialisieren bei Seitenladung
document.addEventListener('DOMContentLoaded', function() {
    // Setze standardmäßig Audio-Modus als aktiv
    setVisualizationMode('audio');
    
    // Setze ersten Audio-Pattern-Button als aktiv
    const audioPatternButtons = document.querySelectorAll('#audio-patterns .pattern-btn');
    if (audioPatternButtons.length > 0) {
        audioPatternButtons.forEach(btn => btn.classList.remove('active'));
        audioPatternButtons[0].classList.add('active');
    }
});
// function updateStatus(message, status = "loading") {
//   const statusDiv = document.getElementById("status");
//   statusDiv.textContent = message;
//   statusDiv.className = `status ${status}`;
// }

// function runSequence(endpoint) {
//   updateStatus(`Führe Sequenz aus...`);

//   fetch("/" + endpoint)
//     .then((response) => response.json())
//     .then((data) => {
//       updateStatus(data.message, "success");
//     })
//     .catch((error) => {
//       updateStatus(`Fehler: ${error}`, "error");
//     });
// }

// function setColor(color) {
//   updateStatus(`Setze LEDs auf Farbe ${color}...`);

//   fetch("/set_color", {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/json",
//     },
//     body: JSON.stringify({ color: color }),
//   })
//     .then((response) => response.json())
//     .then((data) => {
//       updateStatus(data.message, "success");
//     })
//     .catch((error) => {
//       updateStatus(`Fehler: ${error}`, "error");
//     });
// }

// function turnOff() {
//   updateStatus("Schalte LEDs aus...");

//   fetch("/turn_off", {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/json",
//     },
//     body: JSON.stringify({}),
//   })
//     .then((response) => response.json())
//     .then((data) => {
//       updateStatus(data.message, "success");
//     })
//     .catch((error) => {
//       updateStatus(`Fehler: ${error}`, "error");
//     });
// }

// function pulseLEDs() {
//   const colorPicker = document.getElementById("pulsePicker");
//   const color = colorPicker.value;
//   const cycleCount = document.getElementById("cycleCount").value;

//   updateStatus(`Lasse LEDs in ${color} pulsieren...`);

//   fetch("/pulse_leds", {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/json",
//     },
//     body: JSON.stringify({ color: color, cycles: cycleCount }),
//   })
//     .then((response) => response.json())
//     .then((data) => {
//       updateStatus(data.message, "success");
//     })
//     .catch((error) => {
//       updateStatus(`Fehler: ${error}`, "error");
//     });
// }

// function changeColorFromPicker() {
//   const colorPicker = document.getElementById("colorPicker");
//   const color = colorPicker.value;
//   setColor(color);
// }

// function setAmplitudeColor(color) {
//   updateStatus(`Setze Amplituden-Farbe ${color}...`);

//   fetch("/set_amplitude_color", {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/json",
//     },
//     body: JSON.stringify({ color: color }),
//   })
//     .then((response) => response.json())
//     .then((data) => {
//       updateStatus(data.message, "success");
//     })
//     .catch((error) => {
//       updateStatus(`Fehler: ${error}`, "error");
//     });
// }

// function setCustomAmplitudeColor() {
//   const colorPicker = document.getElementById("amplitudeColorPicker");
//   const color = colorPicker.value;
//   setAmplitudeColor(color);
// }
