# Issues Backlog for microbot-unity-udp-prototype

## Issue 01: Test Unity compilation

Goal:
Confirm that `MicroBotNetClient.cs` compiles inside Unity.

Tasks:
- [ ] Create a Unity project.
- [ ] Add the script to `Assets/Scripts`.
- [ ] Attach it to an empty GameObject.
- [ ] Check Unity console.

Acceptance criteria:
- No compile errors.
- Screenshot added to demos/screenshots.

## Issue 02: Run local mock UDP receiver

Goal:
Confirm that the Python mock receiver listens on UDP port 4210.

Tasks:
- [ ] Run `python3 tools/mock_udp_receiver.py`.
- [ ] Confirm it listens without errors.
- [ ] Save terminal output.

Acceptance criteria:
- Receiver output is saved in demos/logs.

## Issue 03: Send first Unity packet

Goal:
Send a packet from Unity to the mock receiver.

Tasks:
- [ ] Configure IP 127.0.0.1.
- [ ] Configure port 4210.
- [ ] Trigger SendPing.
- [ ] Confirm packet appears in terminal.

Acceptance criteria:
- Packet log exists.
- README evidence section is updated.

## Issue 04: Prepare ESP32 receiver plan

Goal:
Write the future ESP32 test plan.

Tasks:
- [ ] Define UDP port.
- [ ] Define packet parser behavior.
- [ ] Define safety rejection behavior.
- [ ] Define timeout stop behavior.

Acceptance criteria:
- ESP32 plan exists.
- Status remains not hardware-validated until tested.
