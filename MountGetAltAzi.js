/* Java Script */
/* Socket Start Packet */
var Out;
sky6RASCOMTele.Connect();

if (sky6RASCOMTele.IsConnected==0)/*Connect failed for some reason*/
{
	Out = "Not connected"
}
else
{
	sky6RASCOMTele.GetAzAlt();
	sky6RASCOMTele.IsTracking();
	obj = {
		az: sky6RASCOMTele.dAz,
		alt: sky6RASCOMTele.dAlt,
		tr: sky6RASCOMTele.IsTracking
	};
	// Out  = String(sky6RASCOMTele.dAz) +" | " + String(sky6RASCOMTele.dAlt);
	Out = JSON.stringify(obj);
}
/* Socket End Packet */
