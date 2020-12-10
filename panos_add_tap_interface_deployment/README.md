# Add IoT-Ready Tap Mode Deployment to NGFW

After CDL is successfully enabled in the NGFW, this skillet simplifies the configuration
necessary to deploy a tap-based sensor to capture log traffic.

Skillet operations includes:

    * capture the inputted ethernet interface name
    * configure the ethernet interface in tap mode 
    * add a tap zone with User-ID enabled
    * add Alert-All security profiles, according to Iron-Skillet
    * add Alert-All security group, according to Iron-Skillet
    * add a CDL- and EAL-ready log forwarding profile
    * add a security rule to allow, alert on, and forward 
        all traffic seen from the tap interface

For skillets running PAN-OS 10.x, _Enable Device-ID on Source Zone_ skillet
can be run with this skillet to enable device visibility. 

After the skillet is loaded and changes committed, ensure that CDL is active and connected
and the various log types are creating and forwarding logs to CDL.

```angular2
show logging-status
```