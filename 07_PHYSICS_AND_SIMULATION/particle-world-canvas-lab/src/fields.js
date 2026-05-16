import { Vec2, clamp } from "./vector.js";

export const PRESETS = {
  calm: {
    label: "Calm orbit",
    mode: "orbit",
    fieldStrength: 0.75,
    damping: 0.991,
    turbulence: 0.12,
    mouseMode: "attract",
  },
  vortex: {
    label: "Vortex",
    mode: "vortex",
    fieldStrength: 1.45,
    damping: 0.987,
    turbulence: 0.22,
    mouseMode: "attract",
  },
  gravity: {
    label: "Gravity well",
    mode: "gravity",
    fieldStrength: 1.65,
    damping: 0.985,
    turbulence: 0.10,
    mouseMode: "attract",
  },
  repulsion: {
    label: "Repulsion field",
    mode: "repulsion",
    fieldStrength: 1.25,
    damping: 0.988,
    turbulence: 0.18,
    mouseMode: "repel",
  },
  swarm: {
    label: "Swarm drift",
    mode: "swarm",
    fieldStrength: 0.95,
    damping: 0.992,
    turbulence: 0.55,
    mouseMode: "attract",
  },
  chaos: {
    label: "Chaos mode",
    mode: "chaos",
    fieldStrength: 2.10,
    damping: 0.981,
    turbulence: 1.35,
    mouseMode: "repel",
  },
};

export function centralField(particle, center, mode, strength, time) {
  const offset = center.sub(particle.position);
  const distanceSquared = Math.max(120, offset.lengthSquared());
  const distance = Math.sqrt(distanceSquared);
  const direction = offset.div(distance);

  if (mode === "vortex") {
    const tangent = direction.perpendicular();
    const inward = direction.mul(0.28);
    return tangent.add(inward).mul((strength * 220) / distance);
  }

  if (mode === "gravity") {
    return direction.mul((strength * 9500) / distanceSquared);
  }

  if (mode === "repulsion") {
    return direction.mul((-strength * 8000) / distanceSquared);
  }

  if (mode === "swarm") {
    const wave = Math.sin(time * 0.9 + particle.position.x * 0.006 + particle.position.y * 0.004);
    const tangent = direction.perpendicular().mul(wave * 0.8);
    return direction.mul((strength * 2600) / distanceSquared).add(tangent.mul(strength * 0.08));
  }

  if (mode === "chaos") {
    const waveA = Math.sin(time * 1.7 + particle.position.y * 0.012);
    const waveB = Math.cos(time * 1.1 + particle.position.x * 0.010);
    return new Vec2(waveA, waveB).mul(strength * 0.34).add(direction.perpendicular().mul(strength * 0.10));
  }

  const tangent = direction.perpendicular();
  return tangent.mul((strength * 90) / distance).add(direction.mul((strength * 1400) / distanceSquared));
}

export function mouseField(particle, mouse, mode, influence) {
  if (!mouse.active) return new Vec2(0, 0);

  const offset = mouse.position.sub(particle.position);
  const distanceSquared = Math.max(160, offset.lengthSquared());
  const distance = Math.sqrt(distanceSquared);
  const direction = offset.div(distance);
  const sign = mode === "repel" ? -1 : 1;

  return direction.mul(sign * influence * 9000 / distanceSquared);
}

export function turbulenceField(particle, amount, time) {
  if (amount <= 0) return new Vec2(0, 0);

  const x = Math.sin(time * 1.7 + particle.position.y * 0.017 + particle.age);
  const y = Math.cos(time * 1.3 + particle.position.x * 0.013 - particle.age * 0.4);

  return new Vec2(x, y).mul(amount * 0.16);
}
