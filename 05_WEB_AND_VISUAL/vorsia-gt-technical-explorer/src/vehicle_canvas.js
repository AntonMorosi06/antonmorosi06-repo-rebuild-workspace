export class VehicleCanvas {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext("2d");
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

  draw(activeSystem, telemetry) {
    this.resize();

    const ctx = this.ctx;
    const width = this.canvas.width;
    const height = this.canvas.height;
    const ratio = window.devicePixelRatio || 1;

    this.frame += 1;

    ctx.clearRect(0, 0, width, height);
    this.drawBackground(ctx, width, height);
    this.drawVehicle(ctx, width, height, activeSystem, telemetry, ratio);
    this.drawOverlayLabels(ctx, width, height, activeSystem, ratio);
  }

  drawBackground(ctx, width, height) {
    const gradient = ctx.createRadialGradient(
      width * 0.5,
      height * 0.58,
      20,
      width * 0.5,
      height * 0.5,
      Math.max(width, height) * 0.65,
    );

    gradient.addColorStop(0, "rgba(255, 77, 95, 0.12)");
    gradient.addColorStop(0.42, "rgba(9, 14, 24, 0.96)");
    gradient.addColorStop(1, "rgba(3, 6, 12, 1)");

    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, width, height);

    ctx.save();
    ctx.strokeStyle = "rgba(148, 163, 184, 0.16)";
    ctx.lineWidth = 1;

    const grid = 42 * (window.devicePixelRatio || 1);
    for (let x = 0; x < width; x += grid) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x + width * 0.05, height);
      ctx.stroke();
    }

    for (let y = 0; y < height; y += grid) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(width, y + height * 0.03);
      ctx.stroke();
    }

    ctx.restore();
  }

  drawVehicle(ctx, width, height, activeSystem, telemetry, ratio) {
    const cx = width * 0.5;
    const cy = height * 0.55;
    const length = width * 0.78;
    const bodyHeight = height * 0.23;
    const nose = cx - length * 0.48;
    const tail = cx + length * 0.48;
    const roofY = cy - bodyHeight * 0.95;
    const beltY = cy - bodyHeight * 0.20;
    const floorY = cy + bodyHeight * 0.48;

    ctx.save();

    ctx.shadowColor = "rgba(255, 77, 95, 0.26)";
    ctx.shadowBlur = 24 * ratio;

    const bodyGradient = ctx.createLinearGradient(nose, cy, tail, cy);
    bodyGradient.addColorStop(0, "rgba(255, 77, 95, 0.72)");
    bodyGradient.addColorStop(0.5, "rgba(220, 230, 255, 0.86)");
    bodyGradient.addColorStop(1, "rgba(103, 215, 255, 0.68)");

    ctx.beginPath();
    ctx.moveTo(nose, beltY);
    ctx.bezierCurveTo(cx - length * 0.35, cy - bodyHeight * 0.96, cx - length * 0.16, roofY, cx + length * 0.02, roofY);
    ctx.bezierCurveTo(cx + length * 0.18, roofY, cx + length * 0.31, cy - bodyHeight * 0.70, tail - length * 0.08, beltY);
    ctx.bezierCurveTo(tail, cy - bodyHeight * 0.05, tail - length * 0.02, floorY, tail - length * 0.12, floorY);
    ctx.lineTo(nose + length * 0.12, floorY);
    ctx.bezierCurveTo(nose + length * 0.03, floorY, nose - length * 0.01, cy, nose, beltY);
    ctx.closePath();

    ctx.fillStyle = bodyGradient;
    ctx.globalAlpha = 0.88;
    ctx.fill();
    ctx.globalAlpha = 1;
    ctx.strokeStyle = "rgba(255,255,255,0.42)";
    ctx.lineWidth = 2.2 * ratio;
    ctx.stroke();

    this.drawCabin(ctx, cx, cy, length, bodyHeight, activeSystem, ratio);
    this.drawWheels(ctx, cx, cy, length, bodyHeight, activeSystem, telemetry, ratio);
    this.drawAeroLines(ctx, cx, cy, length, bodyHeight, activeSystem, telemetry, ratio);
    this.drawSystemHighlight(ctx, cx, cy, length, bodyHeight, activeSystem, ratio);

    ctx.restore();
  }

  drawCabin(ctx, cx, cy, length, bodyHeight, activeSystem, ratio) {
    const active = activeSystem.zone === "cockpit" || activeSystem.zone === "cabin";
    ctx.save();
    ctx.fillStyle = active ? "rgba(183, 148, 255, 0.46)" : "rgba(8, 13, 22, 0.64)";
    ctx.strokeStyle = active ? activeSystem.color : "rgba(255,255,255,0.26)";
    ctx.lineWidth = active ? 3 * ratio : 1.5 * ratio;

    ctx.beginPath();
    ctx.moveTo(cx - length * 0.12, cy - bodyHeight * 0.83);
    ctx.lineTo(cx + length * 0.10, cy - bodyHeight * 0.83);
    ctx.lineTo(cx + length * 0.21, cy - bodyHeight * 0.24);
    ctx.lineTo(cx - length * 0.23, cy - bodyHeight * 0.24);
    ctx.closePath();
    ctx.fill();
    ctx.stroke();
    ctx.restore();
  }

  drawWheels(ctx, cx, cy, length, bodyHeight, activeSystem, telemetry, ratio) {
    const wheelY = cy + bodyHeight * 0.48;
    const frontX = cx - length * 0.31;
    const rearX = cx + length * 0.31;
    const radius = bodyHeight * 0.38;
    const active = activeSystem.zone === "wheels";
    const spin = telemetry.speed / 320 + this.frame * 0.018;

    for (const x of [frontX, rearX]) {
      ctx.save();
      ctx.translate(x, wheelY);
      ctx.rotate(spin);
      ctx.beginPath();
      ctx.fillStyle = "rgba(3, 6, 12, 0.92)";
      ctx.strokeStyle = active ? activeSystem.color : "rgba(255,255,255,0.34)";
      ctx.lineWidth = active ? 4 * ratio : 2 * ratio;
      ctx.arc(0, 0, radius, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();

      for (let spoke = 0; spoke < 6; spoke += 1) {
        ctx.rotate(Math.PI / 3);
        ctx.beginPath();
        ctx.moveTo(0, 0);
        ctx.lineTo(radius * 0.75, 0);
        ctx.stroke();
      }

      ctx.restore();
    }
  }

  drawAeroLines(ctx, cx, cy, length, bodyHeight, activeSystem, telemetry, ratio) {
    const active = activeSystem.zone === "body";
    const intensity = 0.22 + telemetry.aeroLoad / 950;

    ctx.save();
    ctx.globalCompositeOperation = "lighter";
    ctx.strokeStyle = active ? activeSystem.color : `rgba(103, 215, 255, ${intensity})`;
    ctx.lineWidth = active ? 3 * ratio : 1.2 * ratio;

    for (let i = 0; i < 7; i += 1) {
      const y = cy - bodyHeight * 0.75 + i * bodyHeight * 0.22;
      ctx.beginPath();
      ctx.moveTo(cx - length * 0.55, y);
      ctx.bezierCurveTo(cx - length * 0.18, y - 34 * ratio, cx + length * 0.18, y + 34 * ratio, cx + length * 0.55, y);
      ctx.stroke();
    }

    ctx.restore();
  }

  drawSystemHighlight(ctx, cx, cy, length, bodyHeight, activeSystem, ratio) {
    ctx.save();
    ctx.globalCompositeOperation = "lighter";
    ctx.strokeStyle = activeSystem.color;
    ctx.fillStyle = `${activeSystem.color}2a`;
    ctx.lineWidth = 3 * ratio;

    if (activeSystem.zone === "center") {
      ctx.beginPath();
      ctx.roundRect(cx - length * 0.18, cy - bodyHeight * 0.14, length * 0.36, bodyHeight * 0.42, 16 * ratio);
      ctx.fill();
      ctx.stroke();
    }

    if (activeSystem.zone === "body") {
      ctx.beginPath();
      ctx.roundRect(cx - length * 0.45, cy - bodyHeight * 0.42, length * 0.90, bodyHeight * 0.62, 18 * ratio);
      ctx.stroke();
    }

    if (activeSystem.zone === "cabin" || activeSystem.zone === "cockpit") {
      ctx.beginPath();
      ctx.roundRect(cx - length * 0.22, cy - bodyHeight * 0.90, length * 0.44, bodyHeight * 0.72, 18 * ratio);
      ctx.stroke();
    }

    ctx.restore();
  }

  drawOverlayLabels(ctx, width, height, activeSystem, ratio) {
    ctx.save();
    ctx.font = `${14 * ratio}px system-ui`;
    ctx.fillStyle = "rgba(237, 243, 255, 0.86)";
    ctx.fillText(`Active system: ${activeSystem.label}`, 24 * ratio, 34 * ratio);
    ctx.fillStyle = "rgba(154, 168, 189, 0.92)";
    ctx.fillText(`Code: ${activeSystem.code}`, 24 * ratio, 58 * ratio);
    ctx.fillText("Conceptual technical visualization, not CAD", 24 * ratio, height - 28 * ratio);
    ctx.restore();
  }
}
