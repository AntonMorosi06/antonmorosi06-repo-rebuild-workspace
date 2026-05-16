import { clamp, lerp } from "./vector.js";

function rgb(color, alpha = 1) {
  return `rgba(${color[0]}, ${color[1]}, ${color[2]}, ${alpha})`;
}

function particleColor(energy) {
  const cold = [90, 168, 255];
  const hot = [255, 184, 107];
  return [
    Math.round(lerp(cold[0], hot[0], energy)),
    Math.round(lerp(cold[1], hot[1], energy)),
    Math.round(lerp(cold[2], hot[2], energy)),
  ];
}

export class Renderer {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext("2d");
    this.showTrails = true;
    this.showJets = true;
    this.showDebug = true;
    this.trailOpacity = 0.42;
    this.lensingIntensity = 1.0;
  }

  resize() {
    const rect = this.canvas.getBoundingClientRect();
    const ratio = window.devicePixelRatio || 1;
    const width = Math.max(320, Math.floor(rect.width * ratio));
    const height = Math.max(320, Math.floor(rect.height * ratio));

    if (this.canvas.width !== width || this.canvas.height !== height) {
      this.canvas.width = width;
      this.canvas.height = height;
    }

    return { width, height, ratio };
  }

  draw(simulation) {
    const { width, height, ratio } = this.resize();
    simulation.resize(width, height);

    const ctx = this.ctx;
    ctx.clearRect(0, 0, width, height);

    this.drawBackground(ctx, width, height, simulation.frame);
    this.drawLensingRings(ctx, simulation);
    this.drawAccretionGlow(ctx, simulation);

    if (this.showTrails) {
      this.drawTrails(ctx, simulation);
    }

    this.drawParticles(ctx, simulation);
    this.drawShockwaves(ctx, simulation);

    if (this.showJets) {
      this.drawJets(ctx, simulation);
    }

    this.drawEventHorizon(ctx, simulation);
    this.drawDebugText(ctx, simulation, ratio);
  }

  drawBackground(ctx, width, height, frame) {
    const gradient = ctx.createRadialGradient(
      width * 0.5,
      height * 0.5,
      20,
      width * 0.5,
      height * 0.5,
      Math.max(width, height) * 0.78,
    );

    gradient.addColorStop(0, "rgba(18, 24, 39, 0.92)");
    gradient.addColorStop(0.42, "rgba(3, 6, 12, 0.98)");
    gradient.addColorStop(1, "rgba(0, 0, 0, 1)");

    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, width, height);

    ctx.save();
    for (let index = 0; index < 130; index += 1) {
      const x = (index * 127 + frame * 0.22) % width;
      const y = (index * 67) % height;
      const alpha = 0.25 + Math.sin(index + frame * 0.015) * 0.12;
      ctx.fillStyle = `rgba(232, 238, 248, ${alpha})`;
      ctx.beginPath();
      ctx.arc(x, y, index % 7 === 0 ? 1.6 : 0.9, 0, Math.PI * 2);
      ctx.fill();
    }
    ctx.restore();
  }

  drawLensingRings(ctx, simulation) {
    const center = simulation.center;
    const strength = this.lensingIntensity;

    ctx.save();
    ctx.globalCompositeOperation = "lighter";

    for (let i = 0; i < 9; i += 1) {
      const radius = simulation.eventHorizonRadius * (1.45 + i * 0.62);
      const alpha = (0.09 + i * 0.014) * strength;
      ctx.strokeStyle = `rgba(90, 168, 255, ${alpha})`;
      ctx.lineWidth = 1 + strength * 0.8;
      ctx.beginPath();
      ctx.ellipse(center.x, center.y, radius * 1.18, radius * 0.48, -0.18, 0, Math.PI * 2);
      ctx.stroke();
    }

    ctx.restore();
  }

  drawAccretionGlow(ctx, simulation) {
    const ctxGradient = ctx.createRadialGradient(
      simulation.center.x,
      simulation.center.y,
      simulation.eventHorizonRadius,
      simulation.center.x,
      simulation.center.y,
      simulation.accretionRadius * 1.25,
    );

    ctxGradient.addColorStop(0, "rgba(255, 184, 107, 0.18)");
    ctxGradient.addColorStop(0.24, "rgba(90, 168, 255, 0.12)");
    ctxGradient.addColorStop(1, "rgba(90, 168, 255, 0)");

    ctx.fillStyle = ctxGradient;
    ctx.beginPath();
    ctx.arc(simulation.center.x, simulation.center.y, simulation.accretionRadius * 1.35, 0, Math.PI * 2);
    ctx.fill();
  }

  drawTrails(ctx, simulation) {
    ctx.save();
    ctx.globalCompositeOperation = "lighter";

    for (const particle of simulation.particles) {
      if (particle.trail.length < 2) continue;

      const color = particleColor(particle.energy);

      for (let i = 1; i < particle.trail.length; i += 1) {
        const a = particle.trail[i - 1];
        const b = particle.trail[i];
        const factor = i / particle.trail.length;
        ctx.strokeStyle = rgb(color, factor * this.trailOpacity);
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(a.x, a.y);
        ctx.lineTo(b.x, b.y);
        ctx.stroke();
      }
    }

    ctx.restore();
  }

  drawParticles(ctx, simulation) {
    ctx.save();
    ctx.globalCompositeOperation = "lighter";

    for (const particle of simulation.particles) {
      const color = particleColor(particle.energy);
      const radius = particle.radius + particle.energy * 2.2;
      ctx.fillStyle = rgb(color, 0.74 + particle.energy * 0.22);
      ctx.beginPath();
      ctx.arc(particle.position.x, particle.position.y, radius, 0, Math.PI * 2);
      ctx.fill();
    }

    ctx.restore();
  }

  drawShockwaves(ctx, simulation) {
    ctx.save();
    ctx.globalCompositeOperation = "lighter";

    for (const shockwave of simulation.shockwaves) {
      ctx.strokeStyle = `rgba(255, 209, 102, ${shockwave.alpha * 0.82})`;
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.arc(shockwave.position.x, shockwave.position.y, shockwave.radius, 0, Math.PI * 2);
      ctx.stroke();
    }

    ctx.restore();
  }

  drawJets(ctx, simulation) {
    const center = simulation.center;
    const height = this.canvas.height;
    const pulse = 0.5 + 0.5 * Math.sin(simulation.frame * 0.055);

    ctx.save();
    ctx.globalCompositeOperation = "lighter";

    const gradientUp = ctx.createLinearGradient(center.x, center.y, center.x, 0);
    gradientUp.addColorStop(0, `rgba(120, 255, 179, ${0.34 + pulse * 0.20})`);
    gradientUp.addColorStop(1, "rgba(120, 255, 179, 0)");

    ctx.fillStyle = gradientUp;
    ctx.beginPath();
    ctx.moveTo(center.x - 18, center.y);
    ctx.lineTo(center.x + 18, center.y);
    ctx.lineTo(center.x + 58, 0);
    ctx.lineTo(center.x - 58, 0);
    ctx.closePath();
    ctx.fill();

    const gradientDown = ctx.createLinearGradient(center.x, center.y, center.x, height);
    gradientDown.addColorStop(0, `rgba(120, 255, 179, ${0.34 + pulse * 0.20})`);
    gradientDown.addColorStop(1, "rgba(120, 255, 179, 0)");

    ctx.fillStyle = gradientDown;
    ctx.beginPath();
    ctx.moveTo(center.x - 18, center.y);
    ctx.lineTo(center.x + 18, center.y);
    ctx.lineTo(center.x + 58, height);
    ctx.lineTo(center.x - 58, height);
    ctx.closePath();
    ctx.fill();

    ctx.restore();
  }

  drawEventHorizon(ctx, simulation) {
    const center = simulation.center;

    ctx.save();
    ctx.shadowColor = "rgba(90, 168, 255, 0.55)";
    ctx.shadowBlur = 28;
    ctx.fillStyle = "rgba(0, 0, 0, 1)";
    ctx.beginPath();
    ctx.arc(center.x, center.y, simulation.eventHorizonRadius, 0, Math.PI * 2);
    ctx.fill();

    ctx.shadowBlur = 0;
    ctx.strokeStyle = "rgba(90, 168, 255, 0.92)";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.arc(center.x, center.y, simulation.eventHorizonRadius + 4, 0, Math.PI * 2);
    ctx.stroke();
    ctx.restore();
  }

  drawDebugText(ctx, simulation, ratio) {
    if (!this.showDebug) return;

    const stats = simulation.stats();
    const lines = [
      "Black Hole Web Simulation",
      `Particles: ${stats.particles}`,
      `Absorbed: ${stats.absorbedTotal}`,
      `Shockwaves: ${stats.shockwaves}`,
      `Mode: ${stats.spawnMode}`,
      `Avg energy: ${stats.averageEnergy.toFixed(3)}`,
      `Frame: ${stats.frame}`,
    ];

    ctx.save();
    ctx.font = `${14 * ratio}px system-ui`;
    ctx.fillStyle = "rgba(232, 238, 248, 0.88)";

    let y = 24 * ratio;
    for (const line of lines) {
      ctx.fillText(line, 18 * ratio, y);
      y += 20 * ratio;
    }

    ctx.restore();
  }
}
