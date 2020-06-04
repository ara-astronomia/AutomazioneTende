/* Java Script */
/* Socket Start Packet */
/* Set tracking On */
var Out;

sky6RASCOMTele.Connect();


if (sky6RASCOMTele.IsConnected==0)//Connect failed for some reason
{
	Out = "Not connected"
}
else
{
	sky6RASCOMTele.SetTracking(1, 1, 0, 0);
}
/* Socket End Packet */
