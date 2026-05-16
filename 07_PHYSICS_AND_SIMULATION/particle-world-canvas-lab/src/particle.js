import { Vec2, clamp } from "./vector.js";

export class Particle {
  constructor(position, velocity, options = {}) {
    this.position = position;
    this.velocity = velocity;
    this.acceleration = new Vec2(0, 0);
    this.mass = options.mass ?? 1;
    this.radius = options.radius ?? 2;
    this.hue = options.hue ?? 200;
    this.energy = options.energy ?? 0.1;
    this.age = 0;
    this.trail = [];
  }

  applyForce(force) {
    this.acceleration = this.acceleration.add(force.div(Math.max(0.001, this.mass)));
  }

  update(dt, damping, speedScale, width, height) {
    this.velocity = this.velocity.add(this.acceleration.mul(dt * 60 * speedScale));
    this.velocity = this.velocity.mul(damping);
    this.velocity = this.velocity.clampLength(16);
    this.position = this.position.add(this.velocity.mul(dt * 60 * speedScale));
    this.acceleration = new Vec2(0, 0);
    this.age += dt;
    this.energy = clamp(this.velocity.length() / 12, 0, 1);

    this.wrap(width, height);
  }

  wrap(width, height) {
    const margin = 20;

    if (this.position.x < -margin) this.position.x = width + margin;
    if (this.position.x > width + margin) this.position.x = -margin;
    if (this.position.y < -margin) this.position.y = height + margin;
    if (this.position.y > height + margin) this.position.y = -margin;
  }

  remember(maxLength) {
    this.trail.push(this.position.clone());
    if (this.trail.length > maxLength) {
      this.trail.shift();
    }
  }
}
