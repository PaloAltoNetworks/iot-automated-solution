# Move DHCP Server to DHCP Relay

For PAN-OS releases prior to 10.0, Enhanced Application Logging (EAL) is unable
to generate logs when the NGFW is a local DHCP server. Instead DHCP relay is
required to create the requires EAL traffic logs used by Cortex IoT.

This skillet takes the input interface attached to a DHCP server, moves it to a
logical VLAN interface in another virtual router, and updates the original server
interface to use DHCP relay. This then meets the requires for EAL logging of DHCP
traffic.