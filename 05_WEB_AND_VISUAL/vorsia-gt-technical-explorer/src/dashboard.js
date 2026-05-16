export class TelemetryDashboard {
  constructor() {
    this.time = 0;
    this.intensity = 1.0;
    this.aeroBalance = 0.55;
    this.speed = 0;
    this.batteryAssist = 0;
    this.brakeTemp = 0;
    this.aeroLoad = 0;
  }

  reset() {
    this.time = 0;
    this.speed = 0;
    this.batteryAssist = 0;
    this.brakeTemp = 0;
    this.aeroLoad = 0;
  }

  update(deltaSeconds) {
    this.time += deltaSeconds * this.intensity;

    const launchPulse = Math.sin(this.time * 0.82) * 0.5 + 0.5;
    const cornerPulse = Math.sin(this.time * 1.37 + 1.4) * 0.5 + 0.5;
    const brakePulse = Math.sin(this.time * 0.47 + 2.2) * 0.5 + 0.5;

    this.speed = Math.round(80 + launchPulse * 208 + cornerPulse * 42);
    this.batteryAssist = Math.round(18 + launchPulse * 58);
    this.brakeTemp = Math.round(190 + brakePulse * 480 * this.intensity);
    this.aeroLoad = Math.round(180 + this.speed * 1.55 * this.aeroBalance + cornerPulse * 180);

    return this.snapshot();
  }

  snapshot() {
    return {
      speed: this.speed,
      batteryAssist: this.batteryAssist,
      brakeTemp: this.brakeTemp,
      aeroLoad: this.aeroLoad,
      intensity: this.intensity,
      aeroBalance: this.aeroBalance,
    };
  }
}

export function updateTelemetryDOM(snapshot, elements) {
  elements.speedValue.textContent = String(snapshot.speed);
  elements.batteryValue.textContent = String(snapshot.batteryAssist);
  elements.brakeValue.textContent = String(snapshot.brakeTemp);
  elements.aeroValue.textContent = String(snapshot.aeroLoad);

  const downforceLabel = snapshot.aeroBalance < 0.35
    ? "low drag"
    : snapshot.aeroBalance > 0.72
      ? "attack"
      : "balanced";

  elements.downforceMetric.textContent = downforceLabel;
}
