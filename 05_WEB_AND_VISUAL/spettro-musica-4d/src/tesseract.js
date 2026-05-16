export function createTesseractVertices() {
  const vertices = [];

  for (const x of [-1, 1]) {
    for (const y of [-1, 1]) {
      for (const z of [-1, 1]) {
        for (const w of [-1, 1]) {
          vertices.push([x, y, z, w]);
        }
      }
    }
  }

  return vertices;
}

export function createTesseractEdges(vertices) {
  const edges = [];

  for (let i = 0; i < vertices.length; i += 1) {
    for (let j = i + 1; j < vertices.length; j += 1) {
      let diff = 0;
      for (let axis = 0; axis < 4; axis += 1) {
        if (vertices[i][axis] !== vertices[j][axis]) {
          diff += 1;
        }
      }
      if (diff === 1) {
        edges.push([i, j]);
      }
    }
  }

  return edges;
}

function rotatePlane(point, axisA, axisB, angle) {
  const result = [...point];
  const a = point[axisA];
  const b = point[axisB];
  const cos = Math.cos(angle);
  const sin = Math.sin(angle);

  result[axisA] = a * cos - b * sin;
  result[axisB] = a * sin + b * cos;
  return result;
}

export function rotate4D(point, time, speed) {
  let rotated = point;
  rotated = rotatePlane(rotated, 0, 1, time * 0.38 * speed);
  rotated = rotatePlane(rotated, 2, 3, time * 0.31 * speed);
  rotated = rotatePlane(rotated, 0, 3, time * 0.22 * speed);
  rotated = rotatePlane(rotated, 1, 2, time * 0.18 * speed);
  return rotated;
}

export function project4Dto2D(point, width, height, wDepth, scale, energy) {
  const [x, y, z, w] = point;
  const wDistance = wDepth + 2.6;
  const wFactor = wDistance / (wDistance - w * 0.72);
  const zDistance = 3.8;
  const zFactor = zDistance / (zDistance - z * 0.62 * wFactor);

  const finalScale = scale * wFactor * zFactor * (1 + energy * 0.12);

  return {
    x: width / 2 + x * finalScale,
    y: height / 2 + y * finalScale,
    depth: z * zFactor + w * 0.35,
    w,
  };
}

export class TesseractModel {
  constructor() {
    this.vertices = createTesseractVertices();
    this.edges = createTesseractEdges(this.vertices);
  }

  projected(time, width, height, params, energy) {
    return this.vertices.map((vertex) => {
      const rotated = rotate4D(vertex, time, params.rotationSpeed);
      return project4Dto2D(rotated, width, height, params.wDepth, params.scale, energy);
    });
  }
}
