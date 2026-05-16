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
        SendCommand("stop", "{"reason":"unity_operator_stop"}");
    }

    public void SendSetMode(string mode)
    {
        selectedMode = mode;
        SendCommand("set_mode", "{"mode":"" + EscapeJson(mode) + ""}");
    }

    public void SendSetLed(string color)
    {
        SendCommand("set_led", "{"node":" + selectedNode + ","color":"" + EscapeJson(color) + ""}");
    }

    public void SendSetTarget(Vector3 target)
    {
        string payload =
            "{"node":" + selectedNode +
            ","x":" + target.x.ToString("F3", System.Globalization.CultureInfo.InvariantCulture) +
            ","y":" + target.y.ToString("F3", System.Globalization.CultureInfo.InvariantCulture) +
            ","z":" + target.z.ToString("F3", System.Globalization.CultureInfo.InvariantCulture) +
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
            ""seq":" + sequenceNumber + "," +
            ""controller_id":"" + EscapeJson(controllerId) + ""," +
            ""type":"" + EscapeJson(commandType) + ""," +
            ""timestamp_ms":" + CurrentUnixTimeMilliseconds() + "," +
            ""payload":" + payloadJson +
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

        return value.Replace("\\", "\\\\").Replace(""", "\"");
    }
}
