/* Java Script */
/* Socket Start Packet */
var Out;

sky6RASCOMTele.Connect();

if (sky6RASCOMTele.IsConnected == 0)
{
	Out = "Not connected";
}
else
{
	sky6RASCOMTele.GetAzAlt();
	obj = {
		az: sky6RASCOMTele.dAz,
		alt: sky6RASCOMTele.dAlt,
		tr: sky6RASCOMTele.IsTracking
	};

	Out = JSON.stringify(obj);
}
/* Socket End Packet */
