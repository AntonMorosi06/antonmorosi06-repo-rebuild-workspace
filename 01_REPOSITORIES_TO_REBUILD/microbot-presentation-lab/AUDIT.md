# Repository Audit — microbot-presentation-lab

Repository: `AntonMorosi06/microbot-presentation-lab`

Audit date: 2026-06-05

Target classification: `prepared` / `presentation-lab-skeleton` / `pitch-ready candidate after narrative layer`

Recommended next status: `presentation skeleton with claim boundaries`, not yet `final pitch package`

---

## 1. Repository Identity

| Field | Value |
|---|---|
| Repository name | `microbot-presentation-lab` |
| Visibility at audit time | Private |
| Main topic | Presentation, demo, communication and narrative lab for the MicroBot ecosystem |
| Project type | Website/demo/presentation skeleton combining MicroBot web, drone observer concept, gesture concept, ESP32/Wokwi skeletons, simulation, Blender assets and evidence folders |
| Intended audience | Anton, professors, collaborators, portfolio reviewers, technical contacts, future video/storytelling use |
| Public recommendation | Strong candidate after pitch scripts, audience-specific explanations and claim boundaries are added |

## 2. Current Status

| Status | Selected |
|---|---|
| `planned` | yes |
| `prepared` | yes |
| `presentation-lab-skeleton` | yes |
| `mocked` | yes, because webcam/gesture/drone/ESP32/Wokwi/Blender layers are presentation skeletons until validated |
| `validated-offline` | not confirmed |
| `hardware-ready` | partial skeleton only; not main status |
| `hardware-validated` | no |
| `portfolio-ready` | candidate after pitch/narrative files and local run review |
| `privacy-review-required` | medium, because future evidence/photos/videos may be added |

## 3. Audit Result

`microbot-presentation-lab` already has a useful README. It clearly defines the repository as a local-first and GitHub-ready presentation repository for showing the MicroBot ecosystem as an integrated technical demonstrator. It also correctly states that the repository does not prove that the final MicroBot swarm is complete.

The README includes a local run command, a meaningful repository structure, a correct-claim section and an incorrect-claims section. This is a strong starting point.

The main missing layer is not technical structure. The missing layer is presentation strategy: pitch scripts, audience-specific explanations, demo narration, Q&A and claim boundaries written for humans who do not already understand the whole MicroBot ecosystem.

## 4. What Already Works

| Area | Audit interpretation |
|---|---|
| README identity | Strong enough for a skeleton repo. |
| Current status | Present and honest. |
| Local run command | Present. |
| Repository structure | Present and broad. |
| Correct claim section | Present. |
| Incorrect claims section | Present. |
| Next practical actions | Present. |
| Scope awareness | Good: presentation skeleton, not final physical proof. |

## 5. What Is Missing

| Missing item | Why it matters |
|---|---|
| `CURRENT_STATUS.md` | Keep status separate from README and easier to update. |
| `PITCH_SCOPE.md` | Define the actual role of the repo as pitch/demo/narrative lab. |
| `CLAIM_BOUNDARIES.md` | Expand safe/unsafe wording for professors, collaborators, investors and public portfolio. |
| `PITCH_30_60_180_SECONDS.md` | Core reusable pitch material. |
| `DEMO_SCRIPT.md` | Step-by-step demo narration for video/professor/collaborator presentation. |
| `AUDIENCE_VERSIONS.md` | Separate explanations for technical collaborators, professors, recruiters and non-technical viewers. |
| `Q_AND_A.md` | Defensible answers to common skeptical questions. |
| `PUBLICATION_CHECKLIST.md` | Before making public or linking from portfolio. |

## 6. Main Claim Risks

| Risk | Level | Mitigation |
|---|---|---|
| Viewer thinks the full physical system already works | High | Add claim boundaries and demo script disclaimers. |
| Drone observer concept mistaken for flight-validated drone system | High | Mark as concept/presentation skeleton. |
| Gesture/webcam concept mistaken for validated robot control | Medium | Label as interface concept unless evidence exists. |
| ESP32/Wokwi skeleton mistaken for real hardware validation | Medium | Link to `microbot-labs` hardware status boundary. |
| Presentation becomes too broad and confusing | High | Add pitch scripts and audience-specific versions. |

## 7. Required First Files

| Priority | File | Purpose |
|---:|---|---|
| 1 | `CURRENT_STATUS.md` | Separate status document. |
| 2 | `PITCH_SCOPE.md` | Define what this repository is for. |
| 3 | `CLAIM_BOUNDARIES.md` | Safe/unsafe claims for presentation use. |
| 4 | `PITCH_30_60_180_SECONDS.md` | Core pitch scripts. |
| 5 | `DEMO_SCRIPT.md` | Demo narration and walkthrough. |

## 8. Suggested Issues

| Issue title | Purpose |
|---|---|
| Add presentation lab current status | Create `CURRENT_STATUS.md`. |
| Define pitch and demo scope | Create `PITCH_SCOPE.md`. |
| Add presentation claim boundaries | Create `CLAIM_BOUNDARIES.md`. |
| Add 30/60/180 second pitch scripts | Create `PITCH_30_60_180_SECONDS.md`. |
| Add MicroBot demo narration script | Create `DEMO_SCRIPT.md`. |
| Add audience-specific explanation versions | Create `AUDIENCE_VERSIONS.md`. |
| Add skeptical Q&A | Create `Q_AND_A.md`. |

## 9. Recommended Public Description

Safe short description:

```text
MicroBot Presentation Lab is a presentation and demo-narration repository for explaining the MicroBot ecosystem through website, simulation, drone-observer concept, gesture-interface concept, ESP32/Wokwi skeletons, Blender assets and carefully bounded pitch material.
```

Longer safe description:

```text
MicroBot Presentation Lab organizes the communication layer of the MicroBot project. It connects web presentation, simulation concepts, drone-observer ideas, gesture-interface placeholders, ESP32/Wokwi skeletons, Blender visualization and evidence folders into a structured demo narrative. The repository is intended to explain the MicroBot ecosystem clearly while avoiding claims of completed physical swarm validation.
```

## 10. Final Audit Summary

```text
This repository is currently classified as: prepared / presentation-lab-skeleton.

It should not yet be classified as: final pitch package, hardware-validated demo, investor-ready product deck or completed physical system presentation.

The next concrete action is: add status, pitch scope, claim boundaries and first pitch scripts.
```
