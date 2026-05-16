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
