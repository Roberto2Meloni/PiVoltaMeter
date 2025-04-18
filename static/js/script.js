console.log("Script wurde geladen");

// Funktion zum Umschalten des Visualisierungsmodus
function setVisualizationMode(mode, url) {
  console.log(`Wechsle visualisierungsmodus zu: ${mode}`);

  // Aktive Klasse von allen Buttons entfernen
  document.querySelectorAll(".visualization-controls button").forEach((btn) => {
    btn.classList.remove("active");
  });

  // Aktive Klasse zum ausgewählten Button hinzufügen
  document.getElementById(mode + "-mode").classList.add("active");

  // Status aktualisieren
  document.getElementById("status").innerHTML =
    '<i class="fas fa-sync fa-spin"></i> Wechsle zu Modus: ' + mode;

  // API-Aufruf zum Ändern des Modus
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ mode: mode }),
  })
    .then((response) => response.json())
    .then((data) => {
      document.getElementById("status").innerHTML =
        '<i class="fas fa-check-circle"></i> ' + data.message;
    })
    .catch((error) => {
      document.getElementById("status").innerHTML =
        '<i class="fas fa-exclamation-triangle"></i> Fehler beim Umschalten des Modus';
      console.error("Fehler:", error);
    });
}

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
