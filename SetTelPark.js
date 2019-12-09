/* Java Script */
/* Socket Start Packet */
var = Out;
sky6RASCOMTele.Connect();

'/* The target az, alt, change as needed. */
var TargetAz = 360;
var TargetAlt = 0;

if (sky6RASCOMTele.IsConnected==0)/*Connect failed for some reason*/
{
	Out = "Not connected"
}
else
{
	sky6RASCOMTele.SlewToAzAlt(TargetAz, TargetAlt, "");
        console.log("Slew complete");


#questo comando va verrificato dopo aver provato l'installazione del driver Advanced LX200
        sky6RASCOMTele.SetTracking(0, 1, 0, 0);
	console.log("Tracking off");
	obj = {
		t_park,
		trak_off
	};

	Out = JSON.stringify(oby);

}
/* Socket End Packet */
