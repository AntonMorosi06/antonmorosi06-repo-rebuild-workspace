import { Particle } from "./particle.js";
import { PRESETS, centralField, mouseField, turbulenceField } from "./fields.js";
import { Vec2, fromAngle } from "./vector.js";

export class ParticleSimulation {
  constructor(width, height, seed = 42) {
    this.width = width;
    this.height = height;
    this.center = new Vec2(width / 2, height / 2);
    this.randomState = seed;
    this.particles = [];
    this.frame = 0;
    this.paused = false;
    this.presetName = "calm";
    this.mode = "orbit";
    this.targetCount = 520;
    this.fieldStrength = 1.0;
    this.damping = 0.986;
    this.turbulence = 0.35;
    this.mouseInfluence = 1.0;
    this.speedScale = 1.0;
    this.trailLength = 38;
    this.mouseMode = "attract";
    this.mouse = {
      active: false,
      position: new Vec2(width / 2, height / 2),
    };
    this.applyPreset("calm");
    this.reset();
  }

  random() {
    this.randomState = (1664525 * this.randomState + 1013904223) >>> 0;
    return this.randomState / 4294967296;
  }

  randomRange(min, max) {
    return min + (max - min) * this.random();
  }

  resize(width, height) {
    this.width = width;
    this.height = height;
    this.center = new Vec2(width / 2, height / 2);
  }

  applyPreset(name) {
    const preset = PRESETS[name];
    if (!preset) {
      throw new Error(`Unknown preset: ${name}`);
    }

    this.presetName = name;
    this.mode = preset.mode;
    this.fieldStrength = preset.fieldStrength;
    this.damping = preset.damping;
    this.turbulence = preset.turbulence;
    this.mouseMode = preset.mouseMode;
  }

  reset() {
    this.particles = [];
    this.frame = 0;

    for (let i = 0; i < this.targetCount; i += 1) {
      this.spawnParticle();
    }
  }

  spawnParticle() {
    const angle = this.randomRange(0, Math.PI * 2);
    const radius = this.randomRange(40, Math.min(this.width, this.height) * 0.48);
    const position = this.center.add(fromAngle(angle, radius));
    const tangent = position.sub(this.center).perpendicular().normalized();
    const velocity = tangent.mul(this.randomRange(0.4, 3.4)).add(fromAngle(this.randomRange(0, Math.PI * 2), this.randomRange(0.0, 1.1)));

    const particle = new Particle(position, velocity, {
      mass: this.randomRange(0.6, 1.8),
      radius: this.randomRange(1.2, 3.4),
      hue: this.randomRange(180, 280),
      energy: this.randomRange(0.05, 0.7),
    });

    this.particles.push(particle);
    return particle;
  }

  burst(count = 90) {
    for (let i = 0; i < count; i += 1) {
      const angle = this.randomRange(0, Math.PI * 2);
      const position = this.mouse.active
        ? this.mouse.position.clone()
        : this.center.clone();
      const velocity = fromAngle(angle, this.randomRange(2.0, 8.0));
      const particle = new Particle(position, velocity, {
        mass: this.randomRange(0.5, 1.3),
        radius: this.randomRange(1.0, 2.6),
        hue: this.randomRange(160, 330),
        energy: 1.0,
      });
      this.particles.push(particle);
    }
  }

  update(dt) {
    if (this.paused) return;

    this.frame += 1;
    const time = this.frame / 60;

    while (this.particles.length < this.targetCount) {
      this.spawnParticle();
    }

    if (this.particles.length > this.targetCount * 1.16) {
      this.particles.length = Math.floor(this.targetCount * 1.16);
    }

    for (const particle of this.particles) {
      const central = centralField(particle, this.center, this.mode, this.fieldStrength, time);
      const mouseForce = mouseField(particle, this.mouse, this.mouseMode, this.mouseInfluence);
      const turbulence = turbulenceField(particle, this.turbulence, time);

      particle.applyForce(central);
      particle.applyForce(mouseForce);
      particle.applyForce(turbulence);
      particle.update(dt, this.damping, this.speedScale, this.width, this.height);
      particle.remember(this.trailLength);
    }
  }

  stats() {
    let averageSpeed = 0;
    let averageEnergy = 0;

    for (const particle of this.particles) {
      averageSpeed += particle.velocity.length();
      averageEnergy += particle.energy;
    }

    if (this.particles.length > 0) {
      averageSpeed /= this.particles.length;
      averageEnergy /= this.particles.length;
    }

    return {
      particles: this.particles.length,
      averageSpeed,
      averageEnergy,
      frame: this.frame,
      mode: this.mode,
      presetName: this.presetName,
      fieldStrength: this.fieldStrength,
      mouseMode: this.mouseMode,
    };
  }
}
