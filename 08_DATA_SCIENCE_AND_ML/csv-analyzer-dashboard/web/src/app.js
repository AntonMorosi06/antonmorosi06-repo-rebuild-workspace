async function loadReport() {
  const response = await fetch("data/sample_report.json");
  if (!response.ok) {
    throw new Error(`Could not load report: ${response.status}`);
  }
  return response.json();
}

function number(value, digits = 2) {
  if (typeof value !== "number") return String(value);
  return value.toLocaleString(undefined, { maximumFractionDigits: digits });
}

function renderMetrics(report) {
  document.querySelector("#sourceMetric").textContent = report.source || "unknown";
  document.querySelector("#rowMetric").textContent = number(report.row_count, 0);
  document.querySelector("#columnMetric").textContent = number(report.column_count, 0);
  document.querySelector("#missingMetric").textContent = String(report.columns.filter((column) => column.missing_count > 0).length);
  document.querySelector("#correlationMetric").textContent = String(report.correlations.length);
}

function renderColumn(column) {
  const card = document.createElement("article");
  card.className = "column-card";

  const header = document.createElement("header");
  header.innerHTML = `
    <div>
      <h3>${column.name}</h3>
      <p>${column.unique_count} unique values · ${(column.missing_ratio * 100).toFixed(1)}% missing</p>
    </div>
    <span class="type-badge">${column.inferred_type}</span>
  `;

  const stats = document.createElement("div");
  stats.className = "stat-list";

  if (column.numeric_summary) {
    const s = column.numeric_summary;
    stats.innerHTML = `
      <div class="stat-row"><span>Min</span><strong>${number(s.min)}</strong></div>
      <div class="stat-row"><span>Max</span><strong>${number(s.max)}</strong></div>
      <div class="stat-row"><span>Mean</span><strong>${number(s.mean)}</strong></div>
      <div class="stat-row"><span>Median</span><strong>${number(s.median)}</strong></div>
      <div class="stat-row"><span>Stdev</span><strong>${number(s.stdev)}</strong></div>
    `;
  } else {
    const top = column.top_values.slice(0, 5);
    stats.innerHTML = top.map((item) => `
      <div class="stat-row"><span>${item.value}</span><strong>${item.count}</strong></div>
    `).join("");
  }

  card.appendChild(header);
  card.appendChild(stats);
  return card;
}

function renderColumns(report) {
  const container = document.querySelector("#columnsContainer");
  container.innerHTML = "";
  for (const column of report.columns) {
    container.appendChild(renderColumn(column));
  }
}

function renderCorrelations(report) {
  const container = document.querySelector("#correlationsContainer");
  container.innerHTML = "";

  if (!report.correlations.length) {
    container.innerHTML = "<p>No numeric correlations were computed.</p>";
    return;
  }

  for (const item of report.correlations.slice(0, 12)) {
    const div = document.createElement("div");
    div.className = "correlation-item";
    div.innerHTML = `
      <span>${item.column_a} ↔ ${item.column_b}</span>
      <strong>r=${Number(item.correlation).toFixed(4)}</strong>
    `;
    container.appendChild(div);
  }
}

async function main() {
  try {
    const report = await loadReport();
    renderMetrics(report);
    renderColumns(report);
    renderCorrelations(report);
  } catch (error) {
    document.body.innerHTML = `
      <main style="padding: 32px; color: white; font-family: system-ui">
        <h1>Could not load report</h1>
        <p>${error.message}</p>
        <p>Generate web/data/sample_report.json with the Python CLI first.</p>
      </main>
    `;
  }
}

main();
