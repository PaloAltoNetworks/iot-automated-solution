# IoT Configuration Workflow

Helper configuration based on user inputs.

Core items include Cortex Data Lake (CDL) and Enhanced Application Logging (EAL)
activation and configuration.

Specific to IoT will be various options for DHCP configuration.

> Assumption is an existing firewall, licensed, updated with interfaces, zones, 
> and pre-IoT policies already in place

## 10.x and later release

Based on 10.x selection will give the user the option to configure:

* Cortex Data Lake activation and configuration
* Update log forwarding profiles using CDL and EAL
* If a local DHCP server, enable DHCP broadcast session
* Add security policy for DHCP with an associated logging profile


## 9.x release

Based on 9.x section will give the user the option to configure:

* Cortex Data Lake activation and configuration
* Update log forwarding profiles using CDL and EAL
* If a local DHCP server, transition to DHCP relay
* Add security policy for DHCP with an associated logging profile