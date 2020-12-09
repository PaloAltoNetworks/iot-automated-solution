# Add DHCP Security Policy

This skillet creates a security policy to allow the `dhcp` application from 
an inputted source zone to an inputted destination zone with a log forwarding configured.

Once created, this security policy, which is used for IoT visibility, can be moved
either to the top, to the bottom or directly before/after a reference rule.

Skillet operations includes:

    * capture the input name of the log forwarding profile, zones, and rule placement
    * adds a security rule called dhcp-traffic to the rulebase
    * moves the security rule
    
