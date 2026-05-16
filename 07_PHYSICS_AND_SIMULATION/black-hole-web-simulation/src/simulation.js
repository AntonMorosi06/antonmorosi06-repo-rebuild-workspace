import { Particle, Shockwave } from "./particle.js";
import { Vec2, clamp, fromAngle } from "./vector.js";

export const SPAWN_MODES = ["edge", "disk", "spiral", "rain", "cluster"];

export class BlackHoleSimulation {
  constructor(width, height, seed = 42) {
    this.width = width;
    this.height = height;
    this.center = new Vec2(width / 2, height / 2);
    this.massBase = 18500;
    this.massScale = 1;
    this.eventHorizonRadius = 44;
    this.absorptionRadius = 38;
    this.accretionRadius = 230;
    this.softening = 160;
    this.targetParticles = 620;
    this.trailLength = 36;
    this.diskEnergyScale = 1;
    this.spawnMode = "edge";
    this.particles = [];
    this.shockwaves = [];
    this.absorbedTotal = 0;
    this.frame = 0;
    this.paused = false;
    this.randomState = seed;
    this.reset();
  }

  random() {
    this.randomState = (1664525 * this.randomState + 1013904223) >>> 0;
    return this.randomState / 4294967296;
  }

  randomRange(min, max) {
    return min + (max - min) * this.random();
  }

  randomChoice(items) {
    return items[Math.floor(this.random() * items.length)];
  }

  resize(width, height) {
    this.width = width;
    this.height = height;
    this.center = new Vec2(width / 2, height / 2);
  }

  reset() {
    this.particles = [];
    this.shockwaves = [];
    this.absorbedTotal = 0;
    this.frame = 0;

    for (let i = 0; i < this.targetParticles; i += 1) {
      this.spawnParticle(this.spawnMode);
    }
  }

  setSpawnMode(mode) {
    if (!SPAWN_MODES.includes(mode)) {
      throw new Error(`Unknown spawn mode: ${mode}`);
    }
    this.spawnMode = mode;
  }

  spawnParticle(mode = this.spawnMode) {
    let position;
    let velocity;

    if (mode === "disk") {
      const angle = this.randomRange(0, Math.PI * 2);
      const radius = this.randomRange(this.accretionRadius * 0.75, this.accretionRadius * 1.8);
      position = this.center.add(fromAngle(angle, radius));
      const tangent = position.sub(this.center).perpendicular().normalized();
      velocity = tangent.mul(this.randomRange(2.0, 4.4));
    } else if (mode === "spiral") {
      const angle = this.randomRange(0, Math.PI * 2);
      const radius = this.randomRange(this.accretionRadius * 1.05, this.accretionRadius * 2.5);
      position = this.center.add(fromAngle(angle, radius));
      const inward = this.center.sub(position).normalized();
      const tangent = inward.perpendicular();
      velocity = tangent.mul(this.randomRange(2.3, 4.6)).add(inward.mul(this.randomRange(0.5, 1.4)));
    } else if (mode === "rain") {
      position = new Vec2(this.randomRange(0, this.width), this.randomRange(-120, 0));
      const target = this.center.add(new Vec2(this.randomRange(-180, 180), this.randomRange(-90, 90)));
      velocity = target.sub(position).normalized().mul(this.randomRange(1.2, 3.8));
    } else if (mode === "cluster") {
      const angle = this.randomRange(0, Math.PI * 2);
      const cluster = this.center.add(fromAngle(angle, this.randomRange(320, 540)));
      position = cluster.add(new Vec2(this.randomRange(-52, 52), this.randomRange(-52, 52)));
      velocity = this.center.sub(position).normalized().mul(this.randomRange(0.5, 2.6));
    } else {
      const side = this.randomChoice(["left", "right", "top", "bottom"]);
      if (side === "left") position = new Vec2(-30, this.randomRange(0, this.height));
      if (side === "right") position = new Vec2(this.width + 30, this.randomRange(0, this.height));
      if (side === "top") position = new Vec2(this.randomRange(0, this.width), -30);
      if (side === "bottom") position = new Vec2(this.randomRange(0, this.width), this.height + 30);

      const target = this.center.add(new Vec2(this.randomRange(-240, 240), this.randomRange(-180, 180)));
      velocity = target.sub(position).normalized().mul(this.randomRange(1.0, 3.8));
    }

    const particle = new Particle(
      position,
      velocity,
      this.randomRange(1.2, 3.2),
      this.randomRange(0.08, 0.62),
    );

    this.particles.push(particle);
    return particle;
  }

  update(dt) {
    if (this.paused) return;

    this.frame += 1;
    const alive = [];

    for (const particle of this.particles) {
      this.updateParticle(particle, dt);

      if (particle.absorbed) {
        this.absorbedTotal += 1;
        this.shockwaves.push(new Shockwave(particle.position));
      } else if (!this.isFarOutside(particle)) {
        alive.push(particle);
      }
    }

    this.particles = alive;

    for (const shockwave of this.shockwaves) {
      shockwave.update(dt);
    }
    this.shockwaves = this.shockwaves.filter((shockwave) => shockwave.alive);

    while (this.particles.length < this.targetParticles) {
      this.spawnParticle(this.spawnMode);
    }

    if (this.particles.length > this.targetParticles * 1.15) {
      this.particles.length = Math.floor(this.targetParticles * 1.15);
    }
  }

  updateParticle(particle, dt) {
    const offset = this.center.sub(particle.position);
    const radiusSquared = Math.max(offset.lengthSquared(), this.softening);
    const radius = Math.sqrt(radiusSquared);
    const direction = offset.div(radius);

    const gravitationalStrength = (this.massBase * this.massScale) / radiusSquared;
    const acceleration = direction.mul(gravitationalStrength);

    const swirl = direction.perpendicular().mul((this.massBase * this.massScale) / Math.max(radiusSquared * radius * 0.42, 1));

    particle.velocity = particle.velocity.add(acceleration.add(swirl).mul(dt * 60)).clampLength(13.5);
    particle.position = particle.position.add(particle.velocity.mul(dt * 60));
    particle.age += dt;

    const diskFactor = clamp(1 - radius / this.accretionRadius, 0, 1);
    particle.energy = clamp(particle.energy + diskFactor * 0.018 * this.diskEnergyScale, 0, 1);
    particle.remember(this.trailLength);

    if (radius <= this.absorptionRadius) {
      particle.absorbed = true;
    }
  }

  isFarOutside(particle) {
    const margin = 280;
    return (
      particle.position.x < -margin ||
      particle.position.x > this.width + margin ||
      particle.position.y < -margin ||
      particle.position.y > this.height + margin
    );
  }

  burst(count = 110) {
    for (let i = 0; i < count; i += 1) {
      const angle = this.randomRange(0, Math.PI * 2);
      const radius = this.randomRange(this.eventHorizonRadius * 1.15, this.accretionRadius * 0.78);
      const position = this.center.add(fromAngle(angle, radius));
      const velocity = fromAngle(angle, this.randomRange(2.0, 6.6));
      const particle = new Particle(position, velocity, this.randomRange(1.0, 2.4), 1);
      this.particles.push(particle);
    }
  }

  stats() {
    const averageEnergy = this.particles.length
      ? this.particles.reduce((sum, particle) => sum + particle.energy, 0) / this.particles.length
      : 0;

    return {
      particles: this.particles.length,
      absorbedTotal: this.absorbedTotal,
      shockwaves: this.shockwaves.length,
      spawnMode: this.spawnMode,
      averageEnergy,
      frame: this.frame,
      massScale: this.massScale,
    };
  }
}
