import { BlackHoleSimulation } from "./simulation.js";
import { Renderer } from "./renderer.js";
import { UIController } from "./ui.js";

const canvas = document.querySelector("#simulationCanvas");
const renderer = new Renderer(canvas);
const simulation = new BlackHoleSimulation(canvas.width, canvas.height, 42);
const ui = new UIController(simulation, renderer);

let last = performance.now();

function frame(now) {
  const dt = Math.min(0.05, (now - last) / 1000);
  last = now;

  simulation.update(dt);
  renderer.draw(simulation);
  ui.updateTelemetry();

  requestAnimationFrame(frame);
}

requestAnimationFrame(frame);
