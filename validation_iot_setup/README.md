# NGFW IoT Validations

This validation skillet provides a set of key checks to determine if the NGFW is
correctly configured for IoT.

## Cortex Data Lake Validations

Assess CDL-specific configuration and system state including:

    * Logging Service, IoT, and Threat Prevention license
    * Device Certificate status for 10.x 
    * CDL Certifcate status details
    * Global CDL device configuration
    * Log forwarding profiles CDL and EAL configuration

## Topology-Specific IoT Readiness Validations

Assess IoT related configuration for DHCP including:

    * 10.x local DHCP server: is DHCP Broadcast session enabled
    * 9.x local DHCP server: is DHCP relay configured
    * 9.x and 10.x Virtual Wire: is multicast firewalling enabled
