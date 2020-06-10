/* Java Script */
/* Socket Start Packet */
/* The target az, alt, change as needed. */
var TargetAz = "{az}";
var TargetAlt = "{alt}";
var Track = "{tr}";
var Out;

sky6RASCOMTele.Connect();

if (sky6RASCOMTele.IsConnected == 0)//Connect failed for some reason
{{
	Out = "Not connected"
}}
else
{{
  if (TargetAlt && TargetAz) {{
	sky6RASCOMTele.SlewToAzAlt(TargetAz, TargetAlt, "");
	}}
  sky6RASCOMTele.SetTracking(Track, 1, 0, 0);
}}
/* Socket End Packet */
