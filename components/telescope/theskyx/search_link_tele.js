/* Java Script */
/* Socket Start Packet */
var Out;
/* Make a simpler name for output. */
var console = RunJavaScriptOutput;

/* Connect this scriptable object to the mount hardware and the mount hardware to TheSky if not connected already. */
sky6RASCOMTele.Connect();

if (sky6RASCOMTele.IsConnected==1)//Connect failed for some reason
{{
    console.writeLine("Mount is connected.");
}}
else
{{
    /* Search connection */
    while(sky6RASCOMTele.IsConnected) 
    obj={1}
    {
        sky6Web.Sleep(1000);
    }
    console.writeLine("The Sky is on.");
    Out = JSON.stringify(obj);
    
}}

/* Socket End Packet */
