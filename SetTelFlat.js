/* Java Script */
/* Socket Start Packet */
/* Go to Position Flat az, alt, and tracking off */
var TargetAz = "0.5";
var TargetAlt = "2";
var Out;

sky6RASCOMTele.Connect();


if (sky6RASCOMTele.IsConnected==0)//Connect failed for some reason
{
	Out = "Not connected"
}
else
{
	sky6RASCOMTele.SlewToAzAlt(TargetAz, TargetAlt, "");

  sky6RASCOMTele.SetTracking(0, 1, 0, 0);
}
/* Socket End Packet */
