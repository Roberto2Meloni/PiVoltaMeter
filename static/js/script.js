console.log("Script wurde geladen");

console.log("Script wurde geladen");

// Aktualisiere die Anzeige basierend auf der vollständigen Konfiguration
function updateUIFromConfig(config) {
    console.log("UI wird mit folgender Konfiguration aktualisiert:", config);
    
    // Aktualisiere die Statusanzeige
    if (config.display) {
        document.getElementById('current-mode').textContent = config.display.mode_name;
        document.getElementById('current-color').textContent = config.display.color_name;
        document.getElementById('current-pattern').textContent = config.display.pattern_name;
    }
    
    // Modus-Buttons aktualisieren
    document.querySelectorAll('#audio-mode, #static-mode, #off-mode').forEach(btn => {
        btn.classList.remove('active');
    });
    
    const modeButton = document.getElementById(config.visualization_mode + '-mode');
    if (modeButton) {
        modeButton.classList.add('active');
    }
    
    // Farb-Buttons aktualisieren
    document.querySelectorAll('.color-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    const colorButton = document.getElementById('color_' + config.led_color);
    if (colorButton) {
        colorButton.classList.add('active');
    }
    
    // Mustergruppen anzeigen/verstecken basierend auf Modus
    document.querySelectorAll('.pattern-group').forEach(group => {
        group.style.display = 'none';
    });
    
    if (config.visualization_mode === 'off') {
        document.getElementById('off-info').style.display = 'block';
    } else {
        const patternsContainer = document.getElementById(config.visualization_mode + '-patterns');
        if (patternsContainer) {
            patternsContainer.style.display = 'block';
            
            // Pattern-Buttons aktualisieren
            const patternButtons = patternsContainer.querySelectorAll('.pattern-btn');
            patternButtons.forEach(btn => {
                btn.classList.remove('active');
            });
            
            // Das aktuelle Muster als aktiv markieren
            let currentPatternId = '';
            if (config.visualization_mode === 'audio') {
                currentPatternId = config.audio_pattern;
            } else if (config.visualization_mode === 'static') {
                currentPatternId = config.static_pattern;
            }
            
            if (currentPatternId) {
                const currentPatternButton = document.getElementById(currentPatternId);
                if (currentPatternButton) {
                    currentPatternButton.classList.add('active');
                }
            }
        }
    }
}

// Visualisierungsmodus einstellen
function setVisualizationMode(mode, url) {
    // Entferne aktiven Status von allen Modus-Buttons
    document.querySelectorAll('#audio-mode, #static-mode, #off-mode').forEach(btn => {
        btn.classList.remove('active');
    });

    // Füge aktiven Status zum ausgewählten Button hinzu
    document.getElementById(mode + '-mode').classList.add('active');

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
            if (data.status === "success") {
                console.log('Modus erfolgreich geändert:', data.message);
                // Aktualisiere die UI basierend auf der zurückgegebenen Konfiguration
                if (data.config) {
                    updateUIFromConfig(data.config);
                }
            } else {
                console.error('Fehler beim Ändern des Modus:', data.message);
            }
        })
        .catch(error => {
            console.error('Netzwerkfehler:', error);
        });
    }
}

// Muster einstellen
function setPattern(pattern_name, url) {
    console.log("setPattern aufgerufen mit:", pattern_name, url);
    
    // Aktiven Status von allen Muster-Buttons im aktuellen Modus entfernen
    const activeMode = document.querySelector('#audio-mode.active, #static-mode.active, #off-mode.active').id.replace('-mode', '');
    console.log("Aktiver Modus:", activeMode);
    
    if (activeMode !== 'off') {
        document.querySelectorAll('#' + activeMode + '-patterns .pattern-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        
        // Finde den Button anhand der ID, die dem pattern_name entspricht
        const patternButton = document.getElementById(pattern_name);
        console.log("Gefundener Button:", patternButton);
        
        if (patternButton) {
            patternButton.classList.add('active');
            
            // Sende Anfrage an Backend
            if (url) {
                console.log("Sende Anfrage an:", url, "mit Pattern:", pattern_name);
                fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ pattern: pattern_name })
                })
                .then(response => {
                    console.log("Antwort erhalten:", response);
                    return response.json();
                })
                .then(data => {
                    console.log("Verarbeitete Daten:", data);
                    if (data.status === "success") {
                        console.log('Muster erfolgreich geändert:', data.message);
                        // Aktualisiere die UI basierend auf der zurückgegebenen Konfiguration
                        if (data.config) {
                            updateUIFromConfig(data.config);
                        }
                    } else {
                        console.error('Fehler beim Ändern des Musters:', data.message);
                    }
                })
                .catch(error => {
                    console.error('Netzwerkfehler:', error);
                });
            }
        } else {
            console.error("Button mit ID", pattern_name, "nicht gefunden!");
        }
    } else {
        console.log("Im Off-Modus können keine Muster gesetzt werden");
    }
}

// Farbe einstellen
function setColor(color, url) {
    console.log("setColor aufgerufen mit:", color, url);
    
    // Entferne aktiven Status von allen Farb-Buttons
    document.querySelectorAll('.color-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Füge aktiven Status zum ausgewählten Farb-Button hinzu
    const colorButton = document.getElementById('color_' + color);
    if (colorButton) {
        colorButton.classList.add('active');
        
        // Sende Anfrage an Backend, um die Farbe zu ändern
        if (url) {
            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ color: color })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === "success") {
                    console.log('Farbe erfolgreich geändert:', data.message);
                    // Aktualisiere die UI basierend auf der zurückgegebenen Konfiguration
                    if (data.config) {
                        updateUIFromConfig(data.config);
                    }
                } else {
                    console.error('Fehler beim Ändern der Farbe:', data.message);
                }
            })
            .catch(error => {
                console.error('Netzwerkfehler:', error);
            });
        }
    } else {
        console.error("Farb-Button mit ID 'color_" + color + "' nicht gefunden!");
    }
}

// Initialisieren bei Seitenladung
document.addEventListener('DOMContentLoaded', function() {
    console.log("Script wurde geladen");
    
    // Prüfe, ob eine initiale Konfiguration verfügbar ist (vom Server übergeben)
    if (typeof initialConfig !== 'undefined') {
        console.log("Verwende die vom Server bereitgestellte initiale Konfiguration:", initialConfig);
        updateUIFromConfig(initialConfig);
    } else {
        console.log("Keine initiale Konfiguration gefunden, rufe Konfiguration vom Server ab...");
        // Hole die aktuelle Konfiguration vom Server als Fallback
        fetch('/get_current_config')
            .then(response => response.json())
            .then(data => {
                if (data.status === "success" && data.config) {
                    console.log("Konfiguration vom Server erhalten:", data.config);
                    // Aktualisiere die UI basierend auf der Konfiguration
                    updateUIFromConfig(data.config);
                } else {
                    console.error('Fehler beim Laden der Konfiguration:', data);
                    
                    // Fallback-Initialisierung, falls keine Konfiguration geladen werden kann
                    setVisualizationMode('audio');
                    
                    // Setze ersten Audio-Pattern-Button als aktiv
                    const audioPatternButtons = document.querySelectorAll('#audio-patterns .pattern-btn');
                    if (audioPatternButtons.length > 0) {
                        audioPatternButtons.forEach(btn => btn.classList.remove('active'));
                        audioPatternButtons[0].classList.add('active');
                        document.getElementById('current-pattern').textContent = audioPatternButtons[0].textContent.trim();
                    }
                    
                    // Setze Regenbogen-Farbe als aktiv
                    const colorButtons = document.querySelectorAll('.color-btn');
                    if (colorButtons.length > 0) {
                        colorButtons.forEach(btn => btn.classList.remove('active'));
                        document.getElementById('color_rainbow').classList.add('active');
                        document.getElementById('current-color').textContent = document.getElementById('color_rainbow').textContent.trim();
                    }
                }
            })
            .catch(error => {
                console.error('Netzwerkfehler beim Laden der Konfiguration:', error);
                
                // Fallback-Initialisierung bei Netzwerkfehler
                setVisualizationMode('audio');
            });
    }
});

// Im vorhandenen DOMContentLoaded-Listener oder an einer passenden Stelle
document.addEventListener("DOMContentLoaded", function () {
  // Vorhandenen Code beibehalten
  
  // IP-Adressen anzeigen
  updateIpAddresses(initialConfig.display.ip_addresses);
});

// Funktion zum Aktualisieren der IP-Adressen
function updateIpAddresses(ipAddresses) {
  const ipAddressElement = document.getElementById('ip-addresses');
  
  if (ipAddresses && ipAddresses.length > 0) {
    // IP-Adressen formatieren und anzeigen
    ipAddressElement.innerHTML = ipAddresses.join('<br>');
  } else {
    ipAddressElement.textContent = "Keine IP-Adressen gefunden";
  }
}