# Move DHCP Server to DHCP Relay

> **ONLY for PAN-OS releases prior to 10.0 when the firewall is the DHCP Server** 

For PAN-OS releases prior to 10.0, Enhanced Application Logging (EAL) is unable
to generate logs when the NGFW is a local DHCP server. To properly capture DHCP
traffic in EAL logs to be sent to Cortex Data Lake, the local DHCP server must 
be moved to a VLAN interface, and a DHCP relay must be configured. 

This skillet automates this DHCP server configuration. 

Skillet operations includes:

    * populates the web UI with the existing ethernet interfaces
    * capture the input name(s) of the interface with the DHCP server
    * snapshots the current DHCP server configuration
    * moves the DHCP server to a vlan interface
    * deletes the DHCP server from the original ethernet interface
    * creates a DHCP relay on the initial ethernet interface
    * enables routing from the DHCP relay to the DHCP server