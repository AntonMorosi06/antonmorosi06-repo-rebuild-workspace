# Privacy and Safety Rules

This document defines the privacy and safety rules for rebuilding repositories.

The goal is to avoid publishing personal, sensitive, unsafe, misleading or legally risky material while rebuilding the technical portfolio.

## Core Rule

If a repository contains personal, private, credential, security, financial, educational, medical, biometric, camera, certificate, chat or account-related material, it must be marked as:

`privacy-review-required`

It must not be promoted until the review is complete.

## Sensitive Material Checklist

Before publishing, check whether the repository contains:

| Sensitive material | Action |
|---|---|
| API keys, tokens, passwords | Remove immediately and rotate credentials if exposed. |
| `.env` files | Remove and add `.env` to `.gitignore`. |
| Personal certificates | Redact personal IDs, certificate IDs if needed, and private metadata. |
| School or university documents | Check names, class, institution, grades, private notes. |
| Chat exports | Keep private unless fully anonymized and necessary. |
| Screenshots | Remove personal data, email addresses, account balances, private windows. |
| Financial material | Add disclaimers and remove personal account details. |
| Camera or biometric material | Add privacy explanation and avoid exposing real biometric data. |
| Hardware safety material | Add warnings, voltage limits, wiring precautions and test boundaries. |
| Cybersecurity material | Keep only defensive, local and authorized content. |

## Privacy Review Result

Every reviewed repository should receive one of these results:

| Result | Meaning |
|---|---|
| `public-safe` | No sensitive material remains and claims are controlled. |
| `public-safe-with-redactions` | Repository can be public after specific redactions. |
| `private` | Repository should remain private. |
| `archive-only` | Repository should be preserved but not promoted. |
| `extract-only` | Only selected clean files should be extracted into another repository. |

## Hardware Safety Rules

For MicroBot, ESP32, drone, electronics, battery, motor, sensor and actuator repositories:

- include voltage and current assumptions when possible;
- avoid unsafe wiring instructions;
- document power source limits;
- include breadboard/prototype warnings;
- separate mock/simulation from real hardware;
- do not claim hardware validation without test evidence;
- include emergency stop or disconnect logic when relevant;
- do not present untested drone behavior as flight-ready.

## Cybersecurity Safety Rules

Cybersecurity repositories must be defensive and educational.

Allowed:

- local Linux permission checks;
- log review;
- process inspection;
- service inspection;
- local network basics;
- firewall explanation;
- hardening notes;
- authorized lab exercises.

Not allowed for public promotion:

- unauthorized scanning of third-party targets;
- credential theft;
- malware deployment;
- persistence mechanisms;
- phishing content;
- evasion instructions;
- exploit chains against real systems.

## Financial Safety Rules

For investment, finance or e-commerce repositories:

- do not present the project as financial advice;
- do not promise returns;
- do not show personal account balances;
- do not imply regulated financial service unless legally implemented;
- include an educational/demo disclaimer if public.

## Camera and Biometric Safety Rules

For camera, face recognition, biometric or tracking projects:

- avoid publishing real biometric data;
- avoid exposing private images;
- document that demos are local/prototype unless production privacy architecture exists;
- include limitations and false-positive/false-negative risks;
- do not claim secure biometric authentication without proper testing and threat modeling.

## Final Rule

When in doubt, do not publish the raw material.

Extract only the clean, useful, explainable and public-safe part into a dedicated repository.
