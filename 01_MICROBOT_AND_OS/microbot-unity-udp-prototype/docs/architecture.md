# Architecture

The prototype follows a simple communication chain:

Unity scene -> MicroBotNetClient -> UDP packet -> controller endpoint.

The endpoint can initially be a local mock receiver. Later it can become an ESP32 UDP receiver or a bridge into a MicroBot dashboard.

## Unity layer

Unity sends high-level intent commands. It should not send unsafe low-level actuator instructions directly.

Examples:

- ping
- stop
- set_mode
- set_led
- set_target

## UDP layer

UDP is fast and simple, but it is not reliable. Packets may be lost, duplicated or reordered.

For this reason, the packet contains a sequence number and timestamp.

## Controller layer

The controller must validate packets before doing anything physical.

Future controller rules:

- reject malformed packets;
- reject stale packets;
- reject unsafe targets;
- rate-limit commands;
- stop safely on timeout.
