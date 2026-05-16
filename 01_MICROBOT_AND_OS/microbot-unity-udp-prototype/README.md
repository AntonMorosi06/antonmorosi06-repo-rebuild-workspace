# MicroBot Unity UDP Prototype

MicroBot Unity UDP Prototype is a cleaned workspace for the early Unity-to-MicroBot communication concept originally associated with the `AntonMorosi2234/microBot` branch.

The original repository could not be cloned automatically from the terminal because GitHub returned `Repository not found`. This usually means that the source repository is private, the terminal is not authenticated for that account, or the exact repository name is different. For this reason, this cleaned workspace now contains a safe reconstructed baseline rather than an automatic import of the original source.

This project explores how Unity can act as a high-level control surface for MicroBot. The intended flow is:

Unity scene -> MicroBotNetClient -> UDP packet -> local mock receiver or future ESP32 controller.

## Current status

Status: prepared baseline, source clone blocked.

This folder contains:

- `unity/MicroBotNetClient.cs`
- `tools/mock_udp_receiver.py`
- documentation for architecture, UDP protocol and limitations
- issue backlog
- labels
- import failure report

## What this project is

This is an early Unity/UDP communication prototype. Its purpose is to test how a visual or immersive environment could send structured commands to a MicroBot controller.

## What this project is not

This is not hardware validation. It does not prove real ESP32 communication, real MicroBot movement, real docking, wireless swarm behavior or physical actuation.

## Recommended next steps

1. Add `MicroBotNetClient.cs` to a Unity project.
2. Run `tools/mock_udp_receiver.py`.
3. Configure Unity to send packets to `127.0.0.1:4210`.
4. Press test commands in Unity.
5. Save terminal logs under `demos/logs`.
6. Add screenshot evidence.
7. Later, test with ESP32 only after the mock receiver works.
