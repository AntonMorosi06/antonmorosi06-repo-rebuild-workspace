import { TesseractModel } from "./tesseract.js";
import { ParticleField } from "./particle_field.js";

export class VisualLab {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext("2d");
    this.tesseract = new TesseractModel();
    this.particles = new ParticleField(160);
    this.frame = 0;
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
  }

  draw(audio, params, time) {
    this.resize();

    const ctx = this.ctx;
    const width = this.canvas.width;
    const height = this.canvas.height;
    const energy = Math.min(1, audio.energy * params.sensitivity);

    this.frame += 1;

    this.drawBackground(ctx, width, height, energy, time);
    this.drawSpectrum(ctx, width, height, audio, energy);
    this.particles.draw(ctx, width, height, audio, time, params.sensitivity);
    this.drawTesseract(ctx, width, height, params, energy, time);
    this.drawAudioCube(ctx, width, height, audio, energy, time);
  }

  drawBackground(ctx, width, height, energy, time) {
    const gradient = ctx.createRadialGradient(
      width * 0.5,
      height * 0.5,
      10,
      width * 0.5,
      height * 0.5,
      Math.max(width, height) * 0.7,
    );

    gradient.addColorStop(0, `rgba(28, 48, 84, ${0.18 + energy * 0.25})`);
    gradient.addColorStop(0.45, "rgba(8, 13, 22, 0.96)");
    gradient.addColorStop(1, "rgba(3, 6, 12, 1)");

    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, width, height);

    ctx.save();
    ctx.globalAlpha = 0.18 + energy * 0.18;
    ctx.strokeStyle = "rgba(148, 163, 184, 0.20)";
    ctx.lineWidth = 1;

    const grid = 48 * (window.devicePixelRatio || 1);
    const offset = (time * 18) % grid;

    for (let x = -grid + offset; x < width + grid; x += grid) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x + width * 0.08, height);
      ctx.stroke();
    }

    for (let y = -grid + offset; y < height + grid; y += grid) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(width, y + height * 0.04);
      ctx.stroke();
    }

    ctx.restore();
  }

  drawSpectrum(ctx, width, height, audio, energy) {
    const data = audio.frequencyData;
    const barCount = 96;
    const barWidth = width / barCount;

    ctx.save();
    ctx.globalCompositeOperation = "lighter";

    for (let i = 0; i < barCount; i += 1) {
      const value = data[Math.floor(i * data.length / barCount)] / 255;
      const barHeight = value * height * 0.24;
      const x = i * barWidth;
      const y = height - barHeight;
      const hue = 195 + value * 110;

      ctx.fillStyle = `hsla(${hue}, 95%, 64%, ${0.24 + value * 0.52})`;
      ctx.fillRect(x, y, Math.max(1, barWidth - 2), barHeight);
    }

    ctx.restore();
  }

  drawTesseract(ctx, width, height, params, energy, time) {
    const projected = this.tesseract.projected(time, width, height, params, energy);

    ctx.save();
    ctx.globalCompositeOperation = "lighter";
    ctx.lineWidth = 1.2 + energy * 2.4;

    for (const [a, b] of this.tesseract.edges) {
      const p1 = projected[a];
      const p2 = projected[b];
      const depth = (p1.depth + p2.depth) * 0.5;
      const alpha = 0.26 + Math.min(0.62, Math.abs(depth) * 0.18 + energy * 0.36);
      const hue = 205 + p1.w * 35 + energy * 80;

      ctx.beginPath();
      ctx.strokeStyle = `hsla(${hue}, 95%, 68%, ${alpha})`;
      ctx.moveTo(p1.x, p1.y);
      ctx.lineTo(p2.x, p2.y);
      ctx.stroke();
    }

    for (const point of projected) {
      const radius = 3.2 + energy * 6 + Math.abs(point.w) * 1.1;
      ctx.beginPath();
      ctx.fillStyle = `hsla(${260 + point.w * 30}, 96%, 72%, ${0.70 + energy * 0.25})`;
      ctx.arc(point.x, point.y, radius, 0, Math.PI * 2);
      ctx.fill();
    }

    ctx.restore();
  }

  drawAudioCube(ctx, width, height, audio, energy, time) {
    const size = 70 + energy * 90;
    const cx = width - size * 1.7;
    const cy = size * 1.55;
    const angle = time * 0.72;
    const points = [];

    for (const x of [-1, 1]) {
      for (const y of [-1, 1]) {
        for (const z of [-1, 1]) {
          const rx = x * Math.cos(angle) - z * Math.sin(angle);
          const rz = x * Math.sin(angle) + z * Math.cos(angle);
          const perspective = 1.0 / (1.0 + rz * 0.22);
          points.push({
            x: cx + rx * size * perspective,
            y: cy + y * size * perspective,
          });
        }
      }
    }

    const edges = [
      [0, 1], [0, 2], [0, 4], [3, 1], [3, 2], [3, 7],
      [5, 1], [5, 4], [5, 7], [6, 2], [6, 4], [6, 7],
    ];

    ctx.save();
    ctx.globalCompositeOperation = "lighter";
    ctx.strokeStyle = `rgba(120, 255, 179, ${0.35 + energy * 0.45})`;
    ctx.lineWidth = 1.5 + energy * 2;

    for (const [a, b] of edges) {
      ctx.beginPath();
      ctx.moveTo(points[a].x, points[a].y);
      ctx.lineTo(points[b].x, points[b].y);
      ctx.stroke();
    }

    ctx.fillStyle = `rgba(120, 255, 179, ${0.25 + energy * 0.35})`;
    ctx.font = `${12 * (window.devicePixelRatio || 1)}px system-ui`;
    ctx.fillText("AUDIO CUBE", cx - size * 0.7, cy + size * 1.35);
    ctx.restore();
  }
}
