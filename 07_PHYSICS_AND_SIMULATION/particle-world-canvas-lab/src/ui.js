import { PRESETS } from "./fields.js";

export class UIController {
  constructor(simulation, renderer) {
    this.simulation = simulation;
    this.renderer = renderer;

    this.elements = {
      statusDot: document.querySelector("#statusDot"),
      statusLabel: document.querySelector("#statusLabel"),
      particleMetric: document.querySelector("#particleMetric"),
      speedMetric: document.querySelector("#speedMetric"),
      energyMetric: document.querySelector("#energyMetric"),
      presetMetric: document.querySelector("#presetMetric"),
      frameMetric: document.querySelector("#frameMetric"),
      modeMetric: document.querySelector("#modeMetric"),
      mouseMetric: document.querySelector("#mouseMetric"),
      fieldMetric: document.querySelector("#fieldMetric"),
      pauseButton: document.querySelector("#pauseButton"),
      resetButton: document.querySelector("#resetButton"),
      burstButton: document.querySelector("#burstButton"),
      trailsButton: document.querySelector("#trailsButton"),
      debugButton: document.querySelector("#debugButton"),
      mouseModeButton: document.querySelector("#mouseModeButton"),
      presetButtons: document.querySelector("#presetButtons"),
      countSlider: document.querySelector("#countSlider"),
      fieldSlider: document.querySelector("#fieldSlider"),
      dampingSlider: document.querySelector("#dampingSlider"),
      turbulenceSlider: document.querySelector("#turbulenceSlider"),
      trailSlider: document.querySelector("#trailSlider"),
      mouseSlider: document.querySelector("#mouseSlider"),
      speedSlider: document.querySelector("#speedSlider"),
    };

    this.bind();
    this.renderPresetButtons();
    this.syncSliders();
  }

  bind() {
    this.elements.pauseButton.addEventListener("click", () => {
      this.simulation.paused = !this.simulation.paused;
      this.updateLabels();
    });

    this.elements.resetButton.addEventListener("click", () => {
      this.simulation.reset();
    });

    this.elements.burstButton.addEventListener("click", () => {
      this.simulation.burst();
    });

    this.elements.trailsButton.addEventListener("click", () => {
      this.renderer.showTrails = !this.renderer.showTrails;
      this.updateLabels();
    });

    this.elements.debugButton.addEventListener("click", () => {
      this.renderer.showDebug = !this.renderer.showDebug;
      this.updateLabels();
    });

    this.elements.mouseModeButton.addEventListener("click", () => {
      this.simulation.mouseMode = this.simulation.mouseMode === "attract" ? "repel" : "attract";
      this.updateLabels();
    });

    this.elements.countSlider.addEventListener("input", (event) => {
      this.simulation.targetCount = Number(event.target.value);
    });

    this.elements.fieldSlider.addEventListener("input", (event) => {
      this.simulation.fieldStrength = Number(event.target.value);
    });

    this.elements.dampingSlider.addEventListener("input", (event) => {
      this.simulation.damping = Number(event.target.value);
    });

    this.elements.turbulenceSlider.addEventListener("input", (event) => {
      this.simulation.turbulence = Number(event.target.value);
    });

    this.elements.trailSlider.addEventListener("input", (event) => {
      this.renderer.trailOpacity = Number(event.target.value);
    });

    this.elements.mouseSlider.addEventListener("input", (event) => {
      this.simulation.mouseInfluence = Number(event.target.value);
    });

    this.elements.speedSlider.addEventListener("input", (event) => {
      this.simulation.speedScale = Number(event.target.value);
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
      } else if (event.key.toLowerCase() === "t") {
        this.renderer.showTrails = !this.renderer.showTrails;
      } else if (event.key.toLowerCase() === "d") {
        this.renderer.showDebug = !this.renderer.showDebug;
      } else if (["1", "2", "3", "4", "5", "6"].includes(event.key)) {
        const names = Object.keys(PRESETS);
        const index = Number(event.key) - 1;
        const name = names[index];
        if (name) {
          this.simulation.applyPreset(name);
          this.syncSliders();
          this.renderPresetButtons();
        }
      }

      this.updateLabels();
    });
  }

  attachCanvasMouse(canvas) {
    const updateMouse = (event) => {
      const rect = canvas.getBoundingClientRect();
      const ratioX = canvas.width / rect.width;
      const ratioY = canvas.height / rect.height;
      this.simulation.mouse.position.x = (event.clientX - rect.left) * ratioX;
      this.simulation.mouse.position.y = (event.clientY - rect.top) * ratioY;
      this.simulation.mouse.active = true;
    };

    canvas.addEventListener("mousemove", updateMouse);
    canvas.addEventListener("mouseenter", updateMouse);
    canvas.addEventListener("mouseleave", () => {
      this.simulation.mouse.active = false;
    });
    canvas.addEventListener("click", () => {
      this.simulation.burst(50);
    });
  }

  renderPresetButtons() {
    this.elements.presetButtons.innerHTML = "";

    for (const [name, preset] of Object.entries(PRESETS)) {
      const button = document.createElement("button");
      button.type = "button";
      button.textContent = preset.label;
      button.classList.toggle("active", name === this.simulation.presetName);
      button.addEventListener("click", () => {
        this.simulation.applyPreset(name);
        this.syncSliders();
        this.renderPresetButtons();
      });
      this.elements.presetButtons.appendChild(button);
    }
  }

  syncSliders() {
    this.elements.countSlider.value = String(this.simulation.targetCount);
    this.elements.fieldSlider.value = String(this.simulation.fieldStrength);
    this.elements.dampingSlider.value = String(this.simulation.damping);
    this.elements.turbulenceSlider.value = String(this.simulation.turbulence);
    this.elements.trailSlider.value = String(this.renderer.trailOpacity);
    this.elements.mouseSlider.value = String(this.simulation.mouseInfluence);
    this.elements.speedSlider.value = String(this.simulation.speedScale);
  }

  updateLabels() {
    this.elements.pauseButton.textContent = this.simulation.paused ? "Resume" : "Pause";
    this.elements.trailsButton.textContent = this.renderer.showTrails ? "Trails on" : "Trails off";
    this.elements.debugButton.textContent = this.renderer.showDebug ? "Debug on" : "Debug off";
    this.elements.mouseModeButton.textContent = this.simulation.mouseMode === "attract" ? "Mouse attract" : "Mouse repel";

    this.elements.statusDot.classList.toggle("paused", this.simulation.paused);
    this.elements.statusLabel.textContent = this.simulation.paused ? "Paused" : "Running";
  }

  updateTelemetry() {
    const stats = this.simulation.stats();

    this.elements.particleMetric.textContent = String(stats.particles);
    this.elements.speedMetric.textContent = stats.averageSpeed.toFixed(2);
    this.elements.energyMetric.textContent = stats.averageEnergy.toFixed(2);
    this.elements.presetMetric.textContent = stats.presetName;
    this.elements.frameMetric.textContent = String(stats.frame);
    this.elements.modeMetric.textContent = stats.mode;
    this.elements.mouseMetric.textContent = stats.mouseMode;
    this.elements.fieldMetric.textContent = stats.fieldStrength.toFixed(2);

    this.updateLabels();
  }
}
