/* Java Script */
/* Socket Start Packet */
sky6RASCOMTele.Connect();

'/* The target az, alt, change as needed. */
var TargetAz = 1;
var TargetAlt = 1;

if (sky6RASCOMTele.IsConnected==0)/*Connect failed for some reason*/
{
	Out = "Not connected"
}
else
{
	sky6RASCOMTele.SlewToAzAlt(TargetAz, TargetAlt, "");
        /*console.log("Slew complete");*/
        /*sky6RASCOMTele.SetTracking(0, 1, 0, 0);*/
}
/* Socket End Packet */
