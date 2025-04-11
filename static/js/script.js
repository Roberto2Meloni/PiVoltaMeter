function runSequence(endpoint) {
  const statusDiv = document.getElementById("status");
  statusDiv.textContent = "Führe Sequenz aus...";
  statusDiv.className = "status loading";

  fetch("/" + endpoint)
    .then((response) => response.json())
    .then((data) => {
      statusDiv.textContent = data.message;
      statusDiv.className = "status success";
    })
    .catch((error) => {
      statusDiv.textContent = "Fehler: " + error;
      statusDiv.className = "status error";
    });
}

function setColor(color) {
  const statusDiv = document.getElementById("status");

  statusDiv.textContent = "Setze LEDs auf Farbe " + color + "...";
  statusDiv.className = "status loading";

  fetch("/set_color", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ color: color }),
  })
    .then((response) => response.json())
    .then((data) => {
      statusDiv.textContent = data.message;
      statusDiv.className = "status success";
    })
    .catch((error) => {
      statusDiv.textContent = "Fehler: " + error;
      statusDiv.className = "status error";
    });
}

function turnOff() {
  const statusDiv = document.getElementById("status");
  statusDiv.textContent = "Schalte LEDs aus...";
  statusDiv.className = "status loading";

  fetch("/turn_off", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({}),
  })
    .then((response) => response.json())
    .then((data) => {
      statusDiv.textContent = data.message;
      statusDiv.className = "status success";
    })
    .catch((error) => {
      statusDiv.textContent = "Fehler: " + error;
      statusDiv.className = "status error";
    });
}

function pulseLEDs() {
  const colorPicker = document.getElementById("pulsePicker");
  const color = colorPicker.value;
  const cycleCount = document.getElementById("cycleCount").value;
  const statusDiv = document.getElementById("status");

  statusDiv.textContent = "Lasse LEDs in " + color + " pulsieren...";
  statusDiv.className = "status loading";

  fetch("/pulse_leds", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ color: color, cycles: cycleCount }),
  })
    .then((response) => response.json())
    .then((data) => {
      statusDiv.textContent = data.message;
      statusDiv.className = "status success";
    })
    .catch((error) => {
      statusDiv.textContent = "Fehler: " + error;
      statusDiv.className = "status error";
    });
}

function changeColorFromPicker() {
    const colorPicker = document.getElementById("colorPicker");
    const color = colorPicker.value;
    setColor(color);
}