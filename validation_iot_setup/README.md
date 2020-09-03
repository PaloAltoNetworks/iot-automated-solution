# NGFW IoT Validations

This validation skillet provides a set of key checks to determine if the NGFW is
correctly configured for IoT.

## Cortex Data Lake

Assess CDL configuration and system state including:

* Logging Service license
* Certifcate fetch and details
* Global CDL device configuration
* Log forwarding profiles CDL and EAL configuration

## Cortex IoT

Assess IoT related configuration for DHCP including:

* 10.x local DHCP server: is DHCP Broadcast session enabled
* 10.x Virtual Wire: is multicast firewalling enabled
* 9.x DHCP: is DHCP relay configured