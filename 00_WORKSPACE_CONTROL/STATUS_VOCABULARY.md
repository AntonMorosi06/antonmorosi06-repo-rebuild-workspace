# Repository Status Vocabulary

This document defines the official maturity labels used in this rebuild workspace.

The purpose of these labels is to keep every repository technically honest. A project can be valuable even if it is not finished, but the status must be explicit.

## Status Labels

| Status | Meaning | Can be promoted publicly? |
|---|---|---|
| `planned` | The project exists as an idea, outline, roadmap or architecture. Implementation is not complete. | Only as roadmap or concept. |
| `prepared` | The repository has structure or initial documentation, but still needs cleanup, validation or stronger evidence. | Yes, if limitations are clear. |
| `mocked` | The project contains simulated, placeholder, UI-only or predefined behavior. | Yes, only if described as mock/demo. |
| `validated-offline` | The project has been tested locally in a controlled environment. | Yes, if run instructions and evidence exist. |
| `hardware-ready` | The project contains BOM, wiring, firmware, setup instructions or enough material to prepare hardware testing. | Yes, if not described as fully validated. |
| `hardware-validated` | The project has been tested on real hardware and includes evidence. | Yes, strong portfolio status. |
| `source-preserved` | Source material is preserved but not cleaned, validated or ready. | Usually no. Use as source archive. |
| `asset-source-baseline` | Repository mainly contains assets, models, visuals, GLB, media, diagrams or static material. | Yes, if cataloged and not too heavy. |
| `portfolio-ready` | Repository can be shown publicly with README, limitations, evidence and clear setup. | Yes. Preferred status. |
| `privacy-review-required` | Repository may contain personal information, certificates, screenshots, credentials or sensitive notes. | No, not before review. |
| `archive-only` | Repository should be preserved historically and not promoted as polished work. | No, unless clearly marked archive. |

## Status Transition Examples

| From | To | Required action |
|---|---|---|
| `planned` | `prepared` | Add structure, README and concrete scope. |
| `prepared` | `validated-offline` | Run locally and add evidence. |
| `mocked` | `validated-offline` | Make demo reproducible and document mock boundaries. |
| `hardware-ready` | `hardware-validated` | Test real hardware and add photos/logs/results. |
| `source-preserved` | `prepared` | Audit source material and extract clean files. |
| `privacy-review-required` | `prepared` | Remove or redact sensitive material. |
| `prepared` | `portfolio-ready` | Add README, current status, limitations, setup, evidence and roadmap. |

## Required Files by Status

| Target status | Minimum files |
|---|---|
| `prepared` | `README.md`, `CURRENT_STATUS.md` |
| `validated-offline` | `README.md`, `CURRENT_STATUS.md`, `EVIDENCE.md`, setup/run instructions |
| `hardware-ready` | `README.md`, `BOM.md`, `WIRING.md`, `SAFETY.md`, firmware/setup notes |
| `hardware-validated` | all hardware-ready files plus photos, logs, test results or serial output |
| `portfolio-ready` | `README.md`, `CURRENT_STATUS.md`, `KNOWN_LIMITATIONS.md`, `CHANGELOG.md`, `ROADMAP.md`, evidence |

## Claim Boundaries

A repository status must be reflected in the language used in the README.

Use:

- "prototype"
- "simulation"
- "local lab"
- "research workspace"
- "proof of concept"
- "staged development"
- "hardware-ready"
- "validated locally"

Avoid unless fully proven:

- "production-ready"
- "fully autonomous"
- "complete swarm robotics system"
- "secure by design"
- "AI-powered" without explanation
- "hardware-validated" without evidence
- "investment tool" without financial disclaimers
