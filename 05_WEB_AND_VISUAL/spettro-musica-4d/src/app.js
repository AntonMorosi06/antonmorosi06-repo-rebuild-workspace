import { AudioEngine } from "./audio_engine.js";
import { VisualLab } from "./visual_lab.js";

const canvas = document.querySelector("#mainCanvas");
const lab = new VisualLab(canvas);
const audio = new AudioEngine();

const params = {
  wDepth: 1.8,
  rotationSpeed: 0.82,
  sensitivity: 1.35,
  scale: 168,
};

const elements = {
  startMicButton: document.querySelector("#startMicButton"),
  stopMicButton: document.querySelector("#stopMicButton"),
  syntheticButton: document.querySelector("#syntheticButton"),
  resetButton: document.querySelector("#resetButton"),
  wDepthSlider: document.querySelector("#wDepthSlider"),
  rotationSlider: document.querySelector("#rotationSlider"),
  sensitivitySlider: document.querySelector("#sensitivitySlider"),
  audioStatusDot: document.querySelector("#audioStatusDot"),
  audioStatusLabel: document.querySelector("#audioStatusLabel"),
  audioStatusDescription: document.querySelector("#audioStatusDescription"),
  energyValue: document.querySelector("#energyValue"),
  bandValue: document.querySelector("#bandValue"),
  wDepthValue: document.querySelector("#wDepthValue"),
  modeMetric: document.querySelector("#modeMetric"),
  frameMetric: document.querySelector("#frameMetric"),
  particleMetric: document.querySelector("#particleMetric"),
};

function syncSliders() {
  elements.wDepthSlider.value = String(params.wDepth);
  elements.rotationSlider.value = String(params.rotationSpeed);
  elements.sensitivitySlider.value = String(params.sensitivity);
}

function updateStatus(snapshot) {
  const live = snapshot.mode === "microphone";
  elements.audioStatusDot.classList.toggle("live", live);
  elements.audioStatusLabel.textContent = live ? "Microphone live" : "Synthetic mode";
  elements.audioStatusDescription.textContent = live
    ? "Web Audio analyser attivo su input microfono."
    : "Microfono non attivo. Segnale interno simulato.";

  elements.energyValue.textContent = snapshot.energy.toFixed(2);
  elements.bandValue.textContent = snapshot.dominantBand;
  elements.wDepthValue.textContent = params.wDepth.toFixed(2);
  elements.modeMetric.textContent = snapshot.mode;
  elements.frameMetric.textContent = String(lab.frame);
  elements.particleMetric.textContent = String(lab.particles.count);
}

elements.startMicButton.addEventListener("click", async () => {
  try {
    await audio.startMicrophone();
  } catch (error) {
    audio.useSynthetic();
    alert(`Microphone unavailable: ${error.message}`);
  }
});

elements.stopMicButton.addEventListener("click", () => {
  audio.stop();
});

elements.syntheticButton.addEventListener("click", () => {
  audio.useSynthetic();
});

elements.resetButton.addEventListener("click", () => {
  params.wDepth = 1.8;
  params.rotationSpeed = 0.82;
  params.sensitivity = 1.35;
  syncSliders();
});

elements.wDepthSlider.addEventListener("input", (event) => {
  params.wDepth = Number(event.target.value);
});

elements.rotationSlider.addEventListener("input", (event) => {
  params.rotationSpeed = Number(event.target.value);
});

elements.sensitivitySlider.addEventListener("input", (event) => {
  params.sensitivity = Number(event.target.value);
});

let last = performance.now();

function loop(now) {
  const deltaSeconds = Math.min(0.05, (now - last) / 1000);
  last = now;

  const snapshot = audio.update(deltaSeconds);
  lab.draw(snapshot, params, now / 1000);
  updateStatus(snapshot);

  requestAnimationFrame(loop);
}

window.addEventListener("resize", () => lab.resize());

syncSliders();
requestAnimationFrame(loop);
