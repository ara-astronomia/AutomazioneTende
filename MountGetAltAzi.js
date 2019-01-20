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
	obj = {
		az: sky6RASCOMTele.dAz,
		alt: sky6RASCOMTele.dAlt
	};
	// Out  = String(sky6RASCOMTele.dAz) +" | " + String(sky6RASCOMTele.dAlt);
	Out = JSON.stringify(obj);
}
/* Socket End Packet */
