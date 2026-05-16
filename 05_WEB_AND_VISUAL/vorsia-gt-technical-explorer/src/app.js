import { baseSpecs, getSystemById, vehicleSystems } from "./data.js";
import { TelemetryDashboard, updateTelemetryDOM } from "./dashboard.js";
import { VehicleCanvas } from "./vehicle_canvas.js";

const canvas = document.querySelector("#vehicleCanvas");
const vehicleCanvas = new VehicleCanvas(canvas);
const telemetry = new TelemetryDashboard();

let activeSystem = getSystemById("hybrid");
let last = performance.now();

const elements = {
  systemButtons: document.querySelector("#systemButtons"),
  systemTitle: document.querySelector("#systemTitle"),
  systemDescription: document.querySelector("#systemDescription"),
  systemCode: document.querySelector("#systemCode"),
  systemTheme: document.querySelector("#systemTheme"),
  speedValue: document.querySelector("#speedValue"),
  batteryValue: document.querySelector("#batteryValue"),
  brakeValue: document.querySelector("#brakeValue"),
  aeroValue: document.querySelector("#aeroValue"),
  intensitySlider: document.querySelector("#intensitySlider"),
  aeroSlider: document.querySelector("#aeroSlider"),
  resetTelemetryButton: document.querySelector("#resetTelemetryButton"),
  powerMetric: document.querySelector("#powerMetric"),
  torqueMetric: document.querySelector("#torqueMetric"),
  massMetric: document.querySelector("#massMetric"),
  downforceMetric: document.querySelector("#downforceMetric"),
};

function renderSystemButtons() {
  elements.systemButtons.innerHTML = "";

  for (const system of vehicleSystems) {
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = system.label;
    button.dataset.systemId = system.id;
    button.classList.toggle("active", system.id === activeSystem.id);
    button.addEventListener("click", () => {
      activeSystem = getSystemById(system.id);
      updateSystemPanel();
      renderSystemButtons();
    });
    elements.systemButtons.appendChild(button);
  }
}

function updateSystemPanel() {
  elements.systemTitle.textContent = activeSystem.label;
  elements.systemDescription.textContent = activeSystem.description;
  elements.systemCode.textContent = activeSystem.code;
  elements.systemTheme.textContent = activeSystem.theme;
}

function updateSpecStrip() {
  elements.powerMetric.textContent = `${baseSpecs.powerHp} hp`;
  elements.torqueMetric.textContent = `${baseSpecs.torqueNm} Nm`;
  elements.massMetric.textContent = `${baseSpecs.massKg} kg`;
}

elements.intensitySlider.addEventListener("input", (event) => {
  telemetry.intensity = Number(event.target.value);
});

elements.aeroSlider.addEventListener("input", (event) => {
  telemetry.aeroBalance = Number(event.target.value);
});

elements.resetTelemetryButton.addEventListener("click", () => {
  telemetry.reset();
  telemetry.intensity = 1.0;
  telemetry.aeroBalance = 0.55;
  elements.intensitySlider.value = "1.0";
  elements.aeroSlider.value = "0.55";
});

function loop(now) {
  const deltaSeconds = Math.min(0.05, (now - last) / 1000);
  last = now;

  const snapshot = telemetry.update(deltaSeconds);
  updateTelemetryDOM(snapshot, elements);
  vehicleCanvas.draw(activeSystem, snapshot);

  requestAnimationFrame(loop);
}

window.addEventListener("resize", () => vehicleCanvas.resize());

updateSpecStrip();
updateSystemPanel();
renderSystemButtons();
requestAnimationFrame(loop);
