import { SPAWN_MODES } from "./simulation.js";

export class UIController {
  constructor(simulation, renderer) {
    this.simulation = simulation;
    this.renderer = renderer;

    this.elements = {
      statusDot: document.querySelector("#statusDot"),
      statusLabel: document.querySelector("#statusLabel"),
      particlesMetric: document.querySelector("#particlesMetric"),
      absorbedMetric: document.querySelector("#absorbedMetric"),
      modeMetric: document.querySelector("#modeMetric"),
      energyMetric: document.querySelector("#energyMetric"),
      frameMetric: document.querySelector("#frameMetric"),
      shockwaveMetric: document.querySelector("#shockwaveMetric"),
      massMetric: document.querySelector("#massMetric"),
      lensingMetric: document.querySelector("#lensingMetric"),
      pauseButton: document.querySelector("#pauseButton"),
      resetButton: document.querySelector("#resetButton"),
      burstButton: document.querySelector("#burstButton"),
      jetsButton: document.querySelector("#jetsButton"),
      trailsButton: document.querySelector("#trailsButton"),
      debugButton: document.querySelector("#debugButton"),
      modeButtons: document.querySelector("#modeButtons"),
      massSlider: document.querySelector("#massSlider"),
      particleSlider: document.querySelector("#particleSlider"),
      trailSlider: document.querySelector("#trailSlider"),
      energySlider: document.querySelector("#energySlider"),
      lensingSlider: document.querySelector("#lensingSlider"),
    };

    this.bind();
    this.renderModeButtons();
  }

  bind() {
    this.elements.pauseButton.addEventListener("click", () => {
      this.simulation.paused = !this.simulation.paused;
      this.updateButtonLabels();
    });

    this.elements.resetButton.addEventListener("click", () => {
      this.simulation.reset();
    });

    this.elements.burstButton.addEventListener("click", () => {
      this.simulation.burst();
    });

    this.elements.jetsButton.addEventListener("click", () => {
      this.renderer.showJets = !this.renderer.showJets;
      this.updateButtonLabels();
    });

    this.elements.trailsButton.addEventListener("click", () => {
      this.renderer.showTrails = !this.renderer.showTrails;
      this.updateButtonLabels();
    });

    this.elements.debugButton.addEventListener("click", () => {
      this.renderer.showDebug = !this.renderer.showDebug;
      this.updateButtonLabels();
    });

    this.elements.massSlider.addEventListener("input", (event) => {
      this.simulation.massScale = Number(event.target.value);
    });

    this.elements.particleSlider.addEventListener("input", (event) => {
      this.simulation.targetParticles = Number(event.target.value);
    });

    this.elements.trailSlider.addEventListener("input", (event) => {
      this.renderer.trailOpacity = Number(event.target.value);
    });

    this.elements.energySlider.addEventListener("input", (event) => {
      this.simulation.diskEnergyScale = Number(event.target.value);
    });

    this.elements.lensingSlider.addEventListener("input", (event) => {
      this.renderer.lensingIntensity = Number(event.target.value);
    });

    window.addEventListener("keydown", (event) => {
      if (event.target && ["INPUT", "TEXTAREA", "SELECT"].includes(event.target.tagName)) return;

      if (event.code === "Space") {
        event.preventDefault();
        this.simulation.paused = !this.simulation.paused;
      } else if (event.key.toLowerCase() === "r") {
        this.simulation.reset();
      } else if (event.key.toLowerCase() === "b") {
        this.simulation.burst();
      } else if (event.key.toLowerCase() === "j") {
        this.renderer.showJets = !this.renderer.showJets;
      } else if (event.key.toLowerCase() === "t") {
        this.renderer.showTrails = !this.renderer.showTrails;
      } else if (event.key.toLowerCase() === "d") {
        this.renderer.showDebug = !this.renderer.showDebug;
      } else if (["1", "2", "3", "4", "5"].includes(event.key)) {
        const index = Number(event.key) - 1;
        this.simulation.setSpawnMode(SPAWN_MODES[index]);
        this.renderModeButtons();
      }

      this.updateButtonLabels();
    });
  }

  renderModeButtons() {
    this.elements.modeButtons.innerHTML = "";

    for (const mode of SPAWN_MODES) {
      const button = document.createElement("button");
      button.type = "button";
      button.textContent = mode;
      button.classList.toggle("active", mode === this.simulation.spawnMode);
      button.addEventListener("click", () => {
        this.simulation.setSpawnMode(mode);
        this.renderModeButtons();
      });
      this.elements.modeButtons.appendChild(button);
    }
  }

  updateButtonLabels() {
    this.elements.pauseButton.textContent = this.simulation.paused ? "Resume" : "Pause";
    this.elements.jetsButton.textContent = this.renderer.showJets ? "Jets on" : "Jets off";
    this.elements.trailsButton.textContent = this.renderer.showTrails ? "Trails on" : "Trails off";
    this.elements.debugButton.textContent = this.renderer.showDebug ? "Debug on" : "Debug off";

    this.elements.statusDot.classList.toggle("paused", this.simulation.paused);
    this.elements.statusLabel.textContent = this.simulation.paused ? "Paused" : "Running";
  }

  updateTelemetry() {
    const stats = this.simulation.stats();

    this.elements.particlesMetric.textContent = String(stats.particles);
    this.elements.absorbedMetric.textContent = String(stats.absorbedTotal);
    this.elements.modeMetric.textContent = stats.spawnMode;
    this.elements.energyMetric.textContent = stats.averageEnergy.toFixed(2);
    this.elements.frameMetric.textContent = String(stats.frame);
    this.elements.shockwaveMetric.textContent = String(stats.shockwaves);
    this.elements.massMetric.textContent = stats.massScale.toFixed(2);
    this.elements.lensingMetric.textContent = this.renderer.lensingIntensity.toFixed(2);

    this.updateButtonLabels();
  }
}
