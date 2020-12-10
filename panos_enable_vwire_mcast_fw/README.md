# Enable Multicast Firewalling for Virtual Wires


To capture DHCP broadcast session data with a virtual wire configuration, multicast
firewalling must be enabled.

This skillet allows the user to select one or more virtual wires for the configuration
update.


Skillet operations includes:

    * populates the web UI with the existing vwires 
    * capture the input name(s) of the vwires to configure
    * enable Multicast Firewalling on each inputted vwire

> The `iot_get_device_values` skillet (located in the *rest_get_device_values* directory)
> must be run with this skillet to capture the existing vwires. This is easily done in 
> the IoT workflow.