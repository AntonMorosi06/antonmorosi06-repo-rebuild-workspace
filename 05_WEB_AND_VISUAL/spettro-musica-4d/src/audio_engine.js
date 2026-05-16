export class AudioEngine {
  constructor() {
    this.mode = "synthetic";
    this.audioContext = null;
    this.analyser = null;
    this.stream = null;
    this.frequencyData = new Uint8Array(128);
    this.time = 0;
    this.energy = 0;
    this.dominantBand = "synthetic";
  }

  async startMicrophone() {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      throw new Error("getUserMedia is not available in this browser.");
    }

    this.stop();

    this.stream = await navigator.mediaDevices.getUserMedia({ audio: true, video: false });
    this.audioContext = new AudioContext();
    const source = this.audioContext.createMediaStreamSource(this.stream);

    this.analyser = this.audioContext.createAnalyser();
    this.analyser.fftSize = 256;
    this.analyser.smoothingTimeConstant = 0.82;
    this.frequencyData = new Uint8Array(this.analyser.frequencyBinCount);

    source.connect(this.analyser);
    this.mode = "microphone";
  }

  useSynthetic() {
    this.stop();
    this.mode = "synthetic";
  }

  stop() {
    if (this.stream) {
      for (const track of this.stream.getTracks()) {
        track.stop();
      }
    }

    if (this.audioContext) {
      this.audioContext.close().catch(() => {});
    }

    this.stream = null;
    this.audioContext = null;
    this.analyser = null;
    this.mode = "synthetic";
  }

  update(deltaSeconds) {
    this.time += deltaSeconds;

    if (this.mode === "microphone" && this.analyser) {
      this.analyser.getByteFrequencyData(this.frequencyData);
      let sum = 0;
      let maxValue = 0;
      let maxIndex = 0;

      for (let index = 0; index < this.frequencyData.length; index += 1) {
        const value = this.frequencyData[index];
        sum += value;
        if (value > maxValue) {
          maxValue = value;
          maxIndex = index;
        }
      }

      this.energy = Math.min(1, sum / (this.frequencyData.length * 255));
      this.dominantBand = this.bandName(maxIndex);
      return this.snapshot();
    }

    const synthetic = new Uint8Array(128);
    let sum = 0;
    let maxValue = 0;
    let maxIndex = 0;

    for (let index = 0; index < synthetic.length; index += 1) {
      const waveA = Math.sin(this.time * 1.7 + index * 0.13);
      const waveB = Math.sin(this.time * 0.73 + index * 0.047);
      const pulse = Math.sin(this.time * 2.4) * 0.5 + 0.5;
      const value = Math.max(0, Math.min(255, 70 + waveA * 52 + waveB * 34 + pulse * (index % 12)));
      synthetic[index] = value;
      sum += value;
      if (value > maxValue) {
        maxValue = value;
        maxIndex = index;
      }
    }

    this.frequencyData = synthetic;
    this.energy = Math.min(1, sum / (synthetic.length * 255));
    this.dominantBand = this.bandName(maxIndex);
    return this.snapshot();
  }

  bandName(index) {
    if (index < 12) return "sub / bass";
    if (index < 32) return "low-mid";
    if (index < 64) return "mid";
    if (index < 96) return "high-mid";
    return "air";
  }

  snapshot() {
    return {
      mode: this.mode,
      energy: this.energy,
      dominantBand: this.dominantBand,
      frequencyData: this.frequencyData,
    };
  }
}
