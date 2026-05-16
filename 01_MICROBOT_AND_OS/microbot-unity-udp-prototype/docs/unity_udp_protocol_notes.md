# Unity UDP Protocol Notes

The current baseline sends JSON-like UDP packets.

Example command shape:

{
  "seq": 1,
  "controller_id": "unity-controller-01",
  "type": "ping",
  "timestamp_ms": 1730000000000,
  "payload": {}
}

Initial command types:

- ping
- stop
- set_mode
- set_led
- set_target

This protocol is only a v0.1 development format. It is designed to be readable in terminal logs and easy to parse later on ESP32 or in Python.
