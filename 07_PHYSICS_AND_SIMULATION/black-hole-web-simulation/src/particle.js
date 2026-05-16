import { Vec2 } from "./vector.js";

export class Particle {
  constructor(position, velocity, radius = 2, energy = 0.2) {
    this.position = position;
    this.velocity = velocity;
    this.radius = radius;
    this.energy = energy;
    this.age = 0;
    this.absorbed = false;
    this.trail = [];
  }

  remember(maxLength) {
    this.trail.push(this.position.clone());
    if (this.trail.length > maxLength) {
      this.trail.shift();
    }
  }
}

export class Shockwave {
  constructor(position) {
    this.position = position.clone();
    this.radius = 8;
    this.alpha = 1;
    this.speed = 4.2;
  }

  update(dt) {
    this.radius += this.speed * dt * 60;
    this.alpha = Math.max(0, this.alpha - dt * 1.25);
  }

  get alive() {
    return this.alpha > 0.01;
  }
}
