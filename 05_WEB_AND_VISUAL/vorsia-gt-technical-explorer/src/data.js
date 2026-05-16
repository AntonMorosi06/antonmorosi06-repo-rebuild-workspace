export const vehicleSystems = [
  {
    id: "hybrid",
    label: "Hybrid drivetrain",
    code: "VGT-HYB",
    theme: "Power delivery",
    color: "#ff4d5f",
    zone: "center",
    description:
      "Fictional hybrid layout with combustion rear drive and electric front axle assist. The interface uses it to explain launch support, torque fill and regenerative behavior.",
  },
  {
    id: "aero",
    label: "Active aerodynamics",
    code: "VGT-AERO",
    theme: "Downforce management",
    color: "#67d7ff",
    zone: "body",
    description:
      "Conceptual aero system with front splitter, underfloor channels, rear diffuser and adaptive wing. It is represented as a visual storytelling layer, not CFD validation.",
  },
  {
    id: "chassis",
    label: "Carbon chassis",
    code: "VGT-CHS",
    theme: "Structural stiffness",
    color: "#7cffb2",
    zone: "cabin",
    description:
      "Fictional carbon tub and aluminum crash structures. This section frames the vehicle as a lightweight GT concept with safety-cell focused architecture.",
  },
  {
    id: "brakes",
    label: "Brake and thermal system",
    code: "VGT-BRK",
    theme: "Heat control",
    color: "#ffb86b",
    zone: "wheels",
    description:
      "Synthetic brake-by-wire and cooling explanation. The telemetry panel uses brake temperature as a simulated value for dashboard behavior.",
  },
  {
    id: "cockpit",
    label: "Telemetry cockpit",
    code: "VGT-COC",
    theme: "Driver information",
    color: "#b794ff",
    zone: "cockpit",
    description:
      "Driver information layer based on speed, energy assist, brake state and aero load. It is designed like a technical dashboard rather than decorative UI.",
  },
];

export const baseSpecs = {
  powerHp: 920,
  torqueNm: 980,
  massKg: 1480,
  wheelbaseMm: 2720,
  layout: "mid-engine AWD hybrid",
};

export function getSystemById(id) {
  return vehicleSystems.find((system) => system.id === id) || vehicleSystems[0];
}
