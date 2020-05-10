/* Java Script */
/* Socket Start Packet */
/* The target az, alt, change as needed. */
var TargetAz = "{az}";
var TargetAlt = "{alt}";
var Out;

sky6RASCOMTele.Connect();

if (sky6RASCOMTele.IsConnected==0)//Connect failed for some reason
{{
	Out = "Not connected"
}}
else
{{
  sky6RASCOMTele.SlewToAzAlt(TargetAz, TargetAlt, "");
  /*console.log("Slew complete");*/
  sky6RASCOMTele.SetTracking(0, 1, 0, 0);
}}
/* Socket End Packet */
