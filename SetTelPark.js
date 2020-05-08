/* Java Script */
/* Socket Start Packet */
/* Go to park tele and tracking off. */
var TargetAz = "0.1";
var TargetAlt = "0.2";
var Out;

sky6RASCOMTele.Connect();


if (sky6RASCOMTele.IsConnected==0)//Connect failed for some reason
{
	Out = "Not connected"
}
else
{
	sky6RASCOMTele.SlewToAzAlt(TargetAz, TargetAlt, "");
        /*console.log("Slew complete");*/
  sky6RASCOMTele.SetTracking(0, 1, 0, 0);
}
/* Socket End Packet */
