import { lerp } from "./vector.js";

function particleColor(particle) {
  const energy = particle.energy;
  const hue = particle.hue + energy * 42;
  return `hsla(${hue}, 92%, ${62 + energy * 12}%,`;
}

export class Renderer {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext("2d");
    this.showTrails = true;
    this.showDebug = true;
    this.trailOpacity = 0.38;
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

    this.drawBackground(ctx, width, height, simulation);
    this.drawFieldRings(ctx, simulation);
    if (this.showTrails) this.drawTrails(ctx, simulation);
    this.drawParticles(ctx, simulation);
    this.drawMouse(ctx, simulation);
    if (this.showDebug) this.drawDebug(ctx, simulation, ratio);
  }

  drawBackground(ctx, width, height, simulation) {
    const gradient = ctx.createRadialGradient(
      width / 2,
      height / 2,
      20,
      width / 2,
      height / 2,
      Math.max(width, height) * 0.72,
    );

    gradient.addColorStop(0, "rgba(22, 35, 58, 0.94)");
    gradient.addColorStop(0.48, "rgba(5, 9, 20, 0.98)");
    gradient.addColorStop(1, "rgba(0, 0, 0, 1)");

    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, width, height);

    ctx.save();
    ctx.strokeStyle = "rgba(148, 163, 184, 0.10)";
    ctx.lineWidth = 1;

    const grid = 54 * (window.devicePixelRatio || 1);
    const offset = (simulation.frame * 0.22) % grid;

    for (let x = -grid + offset; x < width + grid; x += grid) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x + width * 0.04, height);
      ctx.stroke();
    }

    for (let y = -grid + offset; y < height + grid; y += grid) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(width, y + height * 0.03);
      ctx.stroke();
    }

    ctx.restore();
  }

  drawFieldRings(ctx, simulation) {
    ctx.save();
    ctx.globalCompositeOperation = "lighter";

    const center = simulation.center;
    const base = Math.min(simulation.width, simulation.height) * 0.11;

    for (let i = 1; i <= 7; i += 1) {
      const radius = base * i;
      const alpha = 0.035 + i * 0.006;
      ctx.strokeStyle = `rgba(90, 168, 255, ${alpha})`;
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.arc(center.x, center.y, radius, 0, Math.PI * 2);
      ctx.stroke();
    }

    ctx.restore();
  }

  drawTrails(ctx, simulation) {
    ctx.save();
    ctx.globalCompositeOperation = "lighter";

    for (const particle of simulation.particles) {
      if (particle.trail.length < 2) continue;
      const colorPrefix = particleColor(particle);

      for (let i = 1; i < particle.trail.length; i += 1) {
        const a = particle.trail[i - 1];
        const b = particle.trail[i];
        const factor = i / particle.trail.length;
        ctx.strokeStyle = `${colorPrefix} ${factor * this.trailOpacity})`;
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
      const colorPrefix = particleColor(particle);
      const radius = particle.radius + particle.energy * 2.6;
      ctx.fillStyle = `${colorPrefix} ${0.68 + particle.energy * 0.24})`;
      ctx.beginPath();
      ctx.arc(particle.position.x, particle.position.y, radius, 0, Math.PI * 2);
      ctx.fill();
    }

    ctx.restore();
  }

  drawMouse(ctx, simulation) {
    if (!simulation.mouse.active) return;

    ctx.save();
    ctx.globalCompositeOperation = "lighter";
    const color = simulation.mouseMode === "repel"
      ? "rgba(255, 77, 95, 0.72)"
      : "rgba(120, 255, 179, 0.72)";

    ctx.strokeStyle = color;
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.arc(simulation.mouse.position.x, simulation.mouse.position.y, 46, 0, Math.PI * 2);
    ctx.stroke();

    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.arc(simulation.mouse.position.x, simulation.mouse.position.y, 4, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();
  }

  drawDebug(ctx, simulation, ratio) {
    const stats = simulation.stats();
    const lines = [
      "Particle World Canvas Lab",
      `Particles: ${stats.particles}`,
      `Average speed: ${stats.averageSpeed.toFixed(3)}`,
      `Average energy: ${stats.averageEnergy.toFixed(3)}`,
      `Preset: ${stats.presetName}`,
      `Mode: ${stats.mode}`,
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
