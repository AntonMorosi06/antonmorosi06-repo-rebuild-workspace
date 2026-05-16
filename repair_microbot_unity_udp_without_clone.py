from pathlib import Path
from datetime import datetime
import subprocess
import textwrap

ROOT = Path.home() / "Desktop" / "ANTONMOROSI06_REPO_REBUILD_WORKSPACE"
TARGET = ROOT / "01_MICROBOT_AND_OS" / "microbot-unity-udp-prototype"
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).strip() + "\n", encoding="utf-8")
    print("[OK] wrote", path.relative_to(ROOT))

def run(cmd, cwd=None):
    print("[CMD]", " ".join(cmd))
    return subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)

for folder in [
    "unity",
    "docs",
    "demos/screenshots",
    "demos/logs",
    "issues",
    "labels",
    "archive/original_root_files",
    "tools"
]:
    path = TARGET / folder
    path.mkdir(parents=True, exist_ok=True)
    keep = path / ".gitkeep"
    if not keep.exists():
        keep.write_text("", encoding="utf-8")

write(
    TARGET / "README.md",
    """
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
"""
)

write(
    TARGET / "unity" / "MicroBotNetClient.cs",
    """
using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using UnityEngine;

public class MicroBotNetClient : MonoBehaviour
{
    [Header("Network Target")]
    public string remoteIp = "127.0.0.1";
    public int remotePort = 4210;

    [Header("MicroBot State")]
    public string controllerId = "unity-controller-01";
    public string selectedMode = "idle";
    public int selectedNode = 1;

    private UdpClient udpClient;
    private IPEndPoint remoteEndPoint;
    private int sequenceNumber = 0;

    private void Awake()
    {
        ConfigureEndpoint();
    }

    private void OnEnable()
    {
        ConfigureEndpoint();
    }

    private void OnDisable()
    {
        CloseClient();
    }

    private void OnApplicationQuit()
    {
        CloseClient();
    }

    public void ConfigureEndpoint()
    {
        CloseClient();

        udpClient = new UdpClient();
        remoteEndPoint = new IPEndPoint(IPAddress.Parse(remoteIp), remotePort);

        Debug.Log("[MicroBotNetClient] UDP endpoint configured: " + remoteIp + ":" + remotePort);
    }

    public void SendPing()
    {
        SendCommand("ping", "{}");
    }

    public void SendStop()
    {
        SendCommand("stop", "{\"reason\":\"unity_operator_stop\"}");
    }

    public void SendSetMode(string mode)
    {
        selectedMode = mode;
        SendCommand("set_mode", "{\"mode\":\"" + EscapeJson(mode) + "\"}");
    }

    public void SendSetLed(string color)
    {
        SendCommand("set_led", "{\"node\":" + selectedNode + ",\"color\":\"" + EscapeJson(color) + "\"}");
    }

    public void SendSetTarget(Vector3 target)
    {
        string payload =
            "{\"node\":" + selectedNode +
            ",\"x\":" + target.x.ToString("F3", System.Globalization.CultureInfo.InvariantCulture) +
            ",\"y\":" + target.y.ToString("F3", System.Globalization.CultureInfo.InvariantCulture) +
            ",\"z\":" + target.z.ToString("F3", System.Globalization.CultureInfo.InvariantCulture) +
            "}";

        SendCommand("set_target", payload);
    }

    public void SendCommand(string commandType, string payloadJson)
    {
        if (udpClient == null || remoteEndPoint == null)
        {
            ConfigureEndpoint();
        }

        sequenceNumber += 1;

        string json =
            "{" +
            "\"seq\":" + sequenceNumber + "," +
            "\"controller_id\":\"" + EscapeJson(controllerId) + "\"," +
            "\"type\":\"" + EscapeJson(commandType) + "\"," +
            "\"timestamp_ms\":" + CurrentUnixTimeMilliseconds() + "," +
            "\"payload\":" + payloadJson +
            "}";

        byte[] data = Encoding.UTF8.GetBytes(json);
        udpClient.Send(data, data.Length, remoteEndPoint);

        Debug.Log("[MicroBotNetClient] Sent UDP command: " + json);
    }

    private void CloseClient()
    {
        if (udpClient != null)
        {
            udpClient.Close();
            udpClient = null;
        }
    }

    private static long CurrentUnixTimeMilliseconds()
    {
        DateTimeOffset now = DateTimeOffset.UtcNow;
        return now.ToUnixTimeMilliseconds();
    }

    private static string EscapeJson(string value)
    {
        if (string.IsNullOrEmpty(value))
        {
            return "";
        }

        return value.Replace("\\\\", "\\\\\\\\").Replace("\"", "\\\"");
    }
}
"""
)

write(
    TARGET / "tools" / "mock_udp_receiver.py",
    """
import socket
from datetime import datetime

HOST = "0.0.0.0"
PORT = 4210

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))

print(f"[MicroBot UDP Mock Receiver] Listening on {HOST}:{PORT}")
print("Press CTRL+C to stop.")

try:
    while True:
        data, addr = sock.recvfrom(4096)
        timestamp = datetime.now().isoformat(timespec="seconds")
        text = data.decode("utf-8", errors="replace")
        print(f"[{timestamp}] From {addr}: {text}")
except KeyboardInterrupt:
    print("\\n[MicroBot UDP Mock Receiver] Stopped.")
finally:
    sock.close()
"""
)

write(
    TARGET / "docs" / "source_import_status.md",
    f"""
# Source Import Status

Date:
{now}

Source repository attempted:

AntonMorosi2234/microBot

Result:

The terminal clone failed with:

remote: Repository not found.
fatal: repository not found.

Interpretation:

This does not mean the rebuild workspace is broken. It means the terminal cannot access that source repository by HTTPS. The most likely reasons are:

- the source repository is private;
- the terminal is authenticated only for AntonMorosi06;
- the exact repository name is different;
- the source repository was renamed, deleted or moved.

Action taken:

A clean reconstructed baseline was created manually inside:

01_MICROBOT_AND_OS/microbot-unity-udp-prototype

The original source can still be imported later by manually copying the file or by fixing GitHub authentication.
"""
)

write(
    TARGET / "docs" / "architecture.md",
    """
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
"""
)

write(
    TARGET / "docs" / "unity_udp_protocol_notes.md",
    """
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
"""
)

write(
    TARGET / "docs" / "known_limitations.md",
    """
# Known Limitations

This is a prototype baseline.

Known limitations:

- The original source repository was not cloned automatically.
- Unity compilation must still be tested.
- UDP mock validation must still be performed.
- No ESP32 hardware validation has been performed.
- No encryption or authentication is implemented.
- No real MicroBot actuation is validated.
- Commands are development-level JSON strings, not a final protocol.
- This must only be tested on trusted local networks.
"""
)

write(
    TARGET / "docs" / "mock_validation_guide.md",
    """
# Mock Validation Guide

Step 1:

Run the local UDP receiver.

    cd 01_MICROBOT_AND_OS/microbot-unity-udp-prototype
    python3 tools/mock_udp_receiver.py

Step 2:

Open Unity.

Step 3:

Add `MicroBotNetClient.cs` to `Assets/Scripts`.

Step 4:

Attach the script to an empty GameObject.

Step 5:

Set:

    remoteIp = 127.0.0.1
    remotePort = 4210

Step 6:

Trigger `SendPing`, `SendStop`, `SendSetMode`, `SendSetLed` or `SendSetTarget`.

Step 7:

Confirm the terminal receives packets.

Step 8:

Save terminal output in:

    demos/logs/
"""
)

write(
    TARGET / "docs" / "relation_to_microbot_labs.md",
    """
# Relation to microbot-labs

This repository is an experimental Unity/UDP branch.

microbot-labs remains the clean public baseline for MicroBot documentation, dashboard evidence, communication protocol, validation planning and release notes.

This Unity UDP prototype may later support:

- Unity simulation control;
- VR control;
- gesture interface bridge;
- dashboard-to-controller testing;
- ESP32 command transport experiments.

It should not be merged into microbot-labs until it has mock validation and clear protocol documentation.
"""
)

write(
    TARGET / "issues" / "ISSUES_BACKLOG.md",
    """
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
"""
)

write(
    TARGET / "labels" / "labels.yml",
    """
- name: unity
  color: "1d76db"
  description: "Unity/C# integration"
- name: udp
  color: "5319e7"
  description: "UDP communication"
- name: mock-validation
  color: "fbca04"
  description: "Local receiver or offline validation"
- name: microbot-alignment
  color: "0052cc"
  description: "Relation to MicroBot ecosystem"
- name: hardware-blocked
  color: "fef2c0"
  description: "Requires ESP32 or physical hardware"
- name: documentation
  color: "0366d6"
  description: "README and docs"
- name: cleanup
  color: "c5def5"
  description: "Structure and naming cleanup"
- name: portfolio-ready
  color: "0e8a16"
  description: "Required before public presentation"
"""
)

write(
    TARGET / "CHANGELOG.md",
    f"""
# Changelog

## Unreleased

- Repaired MicroBot Unity UDP workspace after source clone failure.
- Added reconstructed `MicroBotNetClient.cs` baseline.
- Added local Python UDP mock receiver.
- Added source import status report.
- Added architecture notes.
- Added UDP protocol notes.
- Added mock validation guide.
- Added relation to microbot-labs.
- Added issue backlog and labels.

Generated: {now}
"""
)

population_log = ROOT / "05_POPULATION_LOG.md"
old_log = population_log.read_text(encoding="utf-8") if population_log.exists() else "# Population Log\n\n"

write(
    population_log,
    old_log + f"""

## {now}

Repaired second repository workspace after clone failure:

- Target: 01_MICROBOT_AND_OS/microbot-unity-udp-prototype
- Source attempted: AntonMorosi2234/microBot
- Problem: GitHub returned repository not found from terminal clone.
- Action: created reconstructed Unity UDP baseline, mock receiver, documentation, issues and labels.

The workspace can now move forward even without automatic source clone.
"""
)

run(["git", "add", "."], cwd=ROOT)

commit = run(["git", "commit", "-m", "Repair MicroBot Unity UDP prototype workspace"], cwd=ROOT)
if commit.returncode == 0:
    print("[OK] Commit created.")
else:
    print("[WARN] Commit not created. Maybe no changes.")
    print(commit.stdout)
    print(commit.stderr)

push = run(["git", "push", "origin", "main"], cwd=ROOT)
if push.returncode == 0:
    print("[OK] Pushed to origin main.")
else:
    print("[WARN] Push failed.")
    print(push.stdout)
    print(push.stderr)

print("[OK] Repair complete.")
