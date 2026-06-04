# Repository Rebuild Method

This document defines the operating method for rebuilding repositories inside this workspace.

The goal of this workspace is not to copy every old file into a new GitHub account. The goal is to rebuild selected repositories into clean, honest, documented, testable and portfolio-ready projects.

## Core Principle

A repository is not considered finished because files exist. A repository is considered useful when its purpose, real status, limitations, structure, run instructions, evidence and next steps are clear.

This workspace must therefore be used as a controlled staging area. Original material can be studied, classified and extracted from, but original archives must not be copied blindly into public repositories.

## Rebuild Flow

| Step | Action | Output |
|---:|---|---|
| 1 | Identify the source repository or archive. | Source name, source path, source account, source date if known. |
| 2 | Preserve original material without modifying it. | Source marked as `source-preserved`. |
| 3 | Audit the content. | `AUDIT.md` with useful files, generated files, private files and duplicates. |
| 4 | Classify the repository. | Status label: planned, prepared, mocked, validated-offline, hardware-ready, hardware-validated, portfolio-ready, archive-only. |
| 5 | Remove noise. | No `.venv`, no `node_modules`, no logs, no generated output, no secrets, no raw ZIP dumps. |
| 6 | Write documentation. | README, current status, limitations, roadmap, setup instructions. |
| 7 | Add evidence. | Screenshots, command outputs, logs, photos, demo notes, test results. |
| 8 | Create issues. | GitHub issues with acceptance criteria and concrete evidence requirements. |
| 9 | Decide public status. | Public, private, archive-only or privacy-review-required. |
| 10 | Publish or split. | Either keep in staging or promote to a dedicated clean repository. |

## What Must Be True Before Promotion

Before a repository is promoted as a serious portfolio project, it must include:

- `README.md`
- `CURRENT_STATUS.md`
- `KNOWN_LIMITATIONS.md`
- `CHANGELOG.md`
- clear run/setup instructions if it contains executable code
- clear evidence if it claims to be tested
- privacy/safety review if it contains personal, security, hardware, financial or AI-related material

## Claim Control

Every repository must avoid inflated technical claims.

Do not claim hardware validation without real hardware evidence.
Do not claim production readiness without deployment and testing.
Do not claim AI autonomy if the project uses prompts, mock logic or predefined behavior.
Do not claim cybersecurity capability beyond local, defensive, authorized learning.
Do not claim physical proof of higher dimensions from visualization or state-space simulations.

## Commit Rule

Commits should be small and meaningful.

Good commit examples:

- `Add repository audit template`
- `Document current status for linux network lab`
- `Add MicroBot hardware limitation notes`
- `Add ESP32 first prototype test log`

Bad commit examples:

- `stuff`
- `update`
- `final final`
- `all projects`
- `massive upload`

## Recommended First Rebuild Targets

| Order | Repository | Reason |
|---:|---|---|
| 1 | `linux-network-security-lab` | Strongest fast portfolio candidate. Easy to validate with commands and outputs. |
| 2 | `microbot-labs` | Central project, but must be documented with honest staged status. |
| 3 | `primoPrototipo` | Important real hardware evidence repository. |
| 4 | `Microbot-Simulation-Core` | Useful technical simulation proof for MicroBot. |
| 5 | `MICROBOT-ULTRA-WEBSITE` | Strong visual demo once claims are controlled. |
