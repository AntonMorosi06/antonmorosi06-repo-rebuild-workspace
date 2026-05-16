import { ParticleSimulation } from "./simulation.js";
import { Renderer } from "./renderer.js";
import { UIController } from "./ui.js";

const canvas = document.querySelector("#particleCanvas");
const renderer = new Renderer(canvas);
const simulation = new ParticleSimulation(canvas.width, canvas.height, 42);
const ui = new UIController(simulation, renderer);

ui.attachCanvasMouse(canvas);

let last = performance.now();

function loop(now) {
  const dt = Math.min(0.05, (now - last) / 1000);
  last = now;

  simulation.update(dt);
  renderer.draw(simulation);
  ui.updateTelemetry();

  requestAnimationFrame(loop);
}

requestAnimationFrame(loop);
