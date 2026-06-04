# Publication Rules

This document defines the rules for deciding whether a repository can be published, promoted, archived or kept private.

The purpose is to protect the quality of the GitHub profile and avoid inflated, unsafe or unclear project claims.

## General Publication Rule

A repository should be public only when a visitor can understand:

1. what the project is;
2. what actually works;
3. what is simulated, mocked or planned;
4. how to run or inspect it;
5. what the limitations are;
6. what evidence exists;
7. what the next development step is.

If these seven points are not clear, the repository should remain in rebuild status.

## Required Public Repository Files

Every serious public repository should include:

| File | Purpose |
|---|---|
| `README.md` | Main explanation, setup and usage. |
| `CURRENT_STATUS.md` | Honest status of what works and what does not. |
| `KNOWN_LIMITATIONS.md` | Technical, hardware, safety, privacy or scope limitations. |
| `ROADMAP.md` | Next staged improvements. |
| `CHANGELOG.md` | Versioned history of changes. |
| `LICENSE` | License decision, when appropriate. |
| `.gitignore` | Prevents local junk and generated files from entering Git. |

## Files That Must Not Be Published Blindly

Do not publish the following without review:

- `.env` files;
- credentials;
- API keys;
- tokens;
- private notes;
- personal certificates with sensitive information;
- screenshots showing personal data;
- chat exports;
- bank, payment, investment or account information;
- raw ZIP archives;
- `.venv` folders;
- `node_modules`;
- build folders;
- generated logs;
- large binary artifacts;
- unreviewed photos;
- school/university documents containing private details.

## Repository Type Rules

### Robotics and MicroBot repositories

Allowed public language:

- staged robotics prototype;
- simulation-driven development;
- ESP32 hardware-ready prototype;
- swarm robotics research workspace;
- dashboard prototype;
- firmware skeleton;
- local test bench.

Avoid unless proven:

- complete swarm robotics platform;
- autonomous robot swarm;
- production hardware;
- validated drone integration;
- BCI-controlled robotics system;
- programmable matter implementation.

### Cybersecurity repositories

Allowed public language:

- defensive lab;
- local audit;
- Linux permissions study;
- network security learning environment;
- authorized testing;
- log analysis;
- hardening practice.

Avoid:

- offensive exploitation framing;
- unauthorized scanning;
- credential attacks;
- malware behavior;
- real target attack language;
- "hacker tool" claims without safe educational framing.

### AI repositories

Allowed public language:

- AI-assisted workflow;
- prompt orchestration;
- local command center;
- data analysis demo;
- model experiment;
- prototype automation.

Avoid unless proven:

- autonomous AI agent;
- production AI system;
- secure AI platform;
- medically/financially reliable AI;
- guaranteed prediction.

### Physics and dimensional simulation repositories

Allowed public language:

- computational visualization;
- state-space model;
- educational simulation;
- mathematical visualization;
- interactive conceptual model.

Avoid:

- proof of higher physical dimensions;
- new physics claim;
- validated physical theory;
- scientific discovery claim without peer-reviewed support.

### Financial or business repositories

Allowed public language:

- UI demo;
- business prototype;
- landing page concept;
- e-commerce interface demo;
- educational finance interface.

Avoid:

- financial advice;
- guaranteed returns;
- investment recommendation;
- active regulated service;
- real checkout claims unless implemented legally.

## Promotion Checklist

Before promoting a repository as portfolio-ready, check:

| Done | Requirement |
|---|---|
| [ ] | README explains the project clearly. |
| [ ] | Current status is honest. |
| [ ] | Limitations are explicit. |
| [ ] | Run/setup instructions exist if code is executable. |
| [ ] | Evidence exists for every major claim. |
| [ ] | No secrets or credentials are present. |
| [ ] | No private personal data is exposed. |
| [ ] | Generated folders are excluded. |
| [ ] | Heavy files are handled through releases or external storage. |
| [ ] | The repository has a next-step roadmap. |

## Decision Outcomes

| Outcome | Meaning |
|---|---|
| `promote` | Repository can be public-facing and linked in portfolio. |
| `rebuild` | Repository is useful but needs cleanup first. |
| `extract` | Only selected files should be moved into a cleaner repository. |
| `archive` | Preserve but do not promote. |
| `private` | Keep private due to personal or sensitive content. |
| `merge` | Merge useful parts into another repository and avoid duplication. |
