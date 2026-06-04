# Repository Audit Template

Use this template to audit a repository before rebuilding, promoting, archiving or splitting it.

Repository name:
Repository URL:
Audit date:
Auditor:
Source account or archive:
Target status:

---

## 1. Repository Identity

| Field | Value |
|---|---|
| Repository name |  |
| Main topic |  |
| Project type |  |
| Main technologies |  |
| Related ecosystem |  |
| Intended audience |  |
| Public/private recommendation |  |

## 2. Current Status

Select the current real status:

| Status | Selected |
|---|---|
| `planned` | [ ] |
| `prepared` | [ ] |
| `mocked` | [ ] |
| `validated-offline` | [ ] |
| `hardware-ready` | [ ] |
| `hardware-validated` | [ ] |
| `source-preserved` | [ ] |
| `asset-source-baseline` | [ ] |
| `portfolio-ready` | [ ] |
| `privacy-review-required` | [ ] |
| `archive-only` | [ ] |

Explain the status:

```text

```

## 3. What Already Works

| Working element | Evidence | Notes |
|---|---|---|
|  |  |  |

## 4. What Is Mocked, Planned or Incomplete

| Element | Type: mocked/planned/incomplete | Required next step |
|---|---|---|
|  |  |  |

## 5. File and Folder Review

| Path | Keep / remove / move / review | Reason |
|---|---|---|
|  |  |  |

## 6. Generated or Unwanted Files

Check for:

| Item | Present? | Action |
|---|---|---|
| `.venv` | [ ] | Remove from Git. |
| `node_modules` | [ ] | Remove from Git. |
| build folders | [ ] | Remove unless needed for static deploy. |
| logs | [ ] | Remove or move to evidence if meaningful. |
| ZIP/RAR archives | [ ] | Remove from Git or move to release/external storage. |
| binary models/assets | [ ] | Review size and storage strategy. |
| cache files | [ ] | Remove. |
| duplicate files | [ ] | Deduplicate. |

## 7. Privacy Review

| Risk | Present? | Action |
|---|---|---|
| API keys/tokens/secrets | [ ] | Remove and rotate if exposed. |
| `.env` files | [ ] | Remove and ignore. |
| Personal information | [ ] | Redact or keep private. |
| Certificates | [ ] | Redact or move to showcase repository. |
| Chat exports | [ ] | Keep private unless anonymized. |
| Screenshots with private data | [ ] | Redact or remove. |
| Financial/account information | [ ] | Remove. |
| Biometric/camera data | [ ] | Remove or document privacy controls. |

Privacy recommendation:

```text

```

## 8. Safety Review

Required only for hardware, cybersecurity, AI, camera, financial, drone or biometric projects.

| Area | Risk | Required note |
|---|---|---|
| Hardware/electronics |  |  |
| Drone/motors/batteries |  |  |
| Cybersecurity |  |  |
| AI/automation |  |  |
| Camera/biometrics |  |  |
| Finance/business |  |  |

## 9. Documentation Gap

| Required file | Exists? | Action |
|---|---|---|
| `README.md` | [ ] |  |
| `CURRENT_STATUS.md` | [ ] |  |
| `KNOWN_LIMITATIONS.md` | [ ] |  |
| `ROADMAP.md` | [ ] |  |
| `CHANGELOG.md` | [ ] |  |
| setup/run instructions | [ ] |  |
| evidence file/folder | [ ] |  |
| license | [ ] |  |

## 10. Evidence Gap

| Claim | Evidence available? | Evidence needed |
|---|---|---|
|  |  |  |

## 11. Recommended Decision

Select one:

| Decision | Selected |
|---|---|
| Promote as portfolio repository | [ ] |
| Rebuild before promotion | [ ] |
| Extract useful files into another repo | [ ] |
| Keep as source archive | [ ] |
| Keep private | [ ] |
| Merge with another repository | [ ] |
| Delete or deprecate later | [ ] |

Decision explanation:

```text

```

## 12. Next Actions

| Priority | Task | Acceptance criteria |
|---:|---|---|
| 1 |  |  |
| 2 |  |  |
| 3 |  |  |
| 4 |  |  |
| 5 |  |  |

## 13. Suggested GitHub Issues

| Issue title | Labels | Acceptance criteria |
|---|---|---|
|  |  |  |

## 14. Final Audit Summary

```text
This repository is currently classified as: 

It should be handled as:

The next concrete action is:
```
