export class Vec2 {
  constructor(x = 0, y = 0) {
    this.x = x;
    this.y = y;
  }

  clone() {
    return new Vec2(this.x, this.y);
  }

  add(other) {
    return new Vec2(this.x + other.x, this.y + other.y);
  }

  sub(other) {
    return new Vec2(this.x - other.x, this.y - other.y);
  }

  mul(scalar) {
    return new Vec2(this.x * scalar, this.y * scalar);
  }

  div(scalar) {
    if (Math.abs(scalar) < 1e-12) return new Vec2(0, 0);
    return new Vec2(this.x / scalar, this.y / scalar);
  }

  lengthSquared() {
    return this.x * this.x + this.y * this.y;
  }

  length() {
    return Math.sqrt(this.lengthSquared());
  }

  normalized() {
    const value = this.length();
    if (value < 1e-12) return new Vec2(0, 0);
    return this.div(value);
  }

  perpendicular() {
    return new Vec2(-this.y, this.x);
  }

  clampLength(maximum) {
    const current = this.length();
    if (current <= maximum || current < 1e-12) return this;
    return this.normalized().mul(maximum);
  }
}

export function fromAngle(angle, magnitude = 1) {
  return new Vec2(Math.cos(angle) * magnitude, Math.sin(angle) * magnitude);
}

export function clamp(value, min, max) {
  return Math.max(min, Math.min(max, value));
}

export function lerp(a, b, t) {
  return a + (b - a) * clamp(t, 0, 1);
}
