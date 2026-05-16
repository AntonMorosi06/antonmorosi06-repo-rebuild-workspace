export class ParticleField {
  constructor(count = 160) {
    this.count = count;
    this.particles = Array.from({ length: count }, (_, index) => this.createParticle(index));
  }

  createParticle(index) {
    const ring = index / this.count;
    return {
      angle: ring * Math.PI * 2,
      radius: 80 + (index % 40) * 7,
      speed: 0.15 + (index % 17) * 0.012,
      size: 1.2 + (index % 5) * 0.36,
      band: index % 128,
    };
  }

  draw(ctx, width, height, audio, time, sensitivity) {
    const data = audio.frequencyData;
    ctx.save();
    ctx.globalCompositeOperation = "lighter";

    for (const particle of this.particles) {
      const bandValue = data[particle.band % data.length] / 255;
      const energyPush = bandValue * 180 * sensitivity;
      const angle = particle.angle + time * particle.speed;
      const radius = particle.radius + energyPush;
      const x = width / 2 + Math.cos(angle) * radius;
      const y = height / 2 + Math.sin(angle * 0.92) * radius * 0.62;
      const alpha = 0.22 + bandValue * 0.62;
      const hue = 200 + bandValue * 95 + particle.band * 0.6;

      ctx.beginPath();
      ctx.fillStyle = `hsla(${hue}, 92%, 68%, ${alpha})`;
      ctx.arc(x, y, particle.size + bandValue * 3.2, 0, Math.PI * 2);
      ctx.fill();
    }

    ctx.restore();
  }
}
