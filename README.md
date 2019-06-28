# AzoSpam
Python Script to flood AzoRult 3.3 panels with legit looking fake data. The aim of this project is to create data that looks as legitimate as possible to make it hard for the attacker to distinguish between real and fake data and to make the whole dataset unusable.

![alt text](https://github.com/hariomenkel/AzoSpam/blob/master/azospam.gif?raw=true)

Note: This project ist still work in progress!

# Prerequisites
Please install Tor before using this script and make sure it is running and listening on Port 9050

Afterwards install the following package:<BR>
<BR>
`pip install PySocks`<BR>
`pip install stem`<BR>
`pip install requests`<BR>
<BR>  
Please follow these steps to make sure this script is able to change the TOR IP programmatically<BR>
<BR>
`$ tor --hash-password MyStr0n9P#D`<BR>
`16:160103B8D7BA7CFA605C9E99E5BB515D9AE71D33B3D01CE0E7747AD0DC`<BR>
<BR>
Add this value to `/etc/torrc` for the value `HashedControlPassword` so it reads<BR>
`HashedControlPassword 16:160103B8D7BA7CFA605C9E99E5BB515D9AE71D33B3D01CE0E7747AD0DC`<BR>
<BR>
Afterwards uncomment the line<BR>
`ControlPort 9051`<BR>
<BR>
and finally restart tor service to make changes take effect<BR>
`$ sudo service tor restart`
  
 
  
