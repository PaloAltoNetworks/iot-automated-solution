# IoT Automated Solutions

Collection of content to help automate NGFW IoT deployments, configuration, and
traffic generation

More elements coming soon...


## IoT Configuration Workflow

Coming soon...

Working in tandem with the content in 
[panos-logging-skillets](https://github.com/PaloAltoNetworks/panos-logging-skillets)
to help simplify NGFW IoT configuration.

The workflow provides a simple web form menu to select elements for Cortex Data Lake
and IoT readiness including:

    * Cortex Data Lake (CDL) implementation Ansible playbook
    * Update log-forwarding profiles with CDL and Enhancement Application logging
    * For 10.x NGFW DHCP servers, enable DHCP session broadcast
    * For pre-10.x NGFW DHCP servers, convert to a logic interface server and DHCP relay
    * Add a DHCP security policy for visbility
    * Configuration/system validation checks for CDL and IoT configuration elements
    
## IoT Configuration Skillets

Coming soon...

Working in tandem with the workflow, simple configuration skillets designed to 
update the NGFW configuration to be CDL/IoT ready.

## IoT Validation Skillet

Coming soon...

Validate key CDL and IoT NGFW elements to help users discover missing elements
required for IoT readiness

## IoT POC built on HomeSkillet Add-on Configuration

Augment the HomeSkillet configuration for an IoT configuration and POC.

    * Leverage the IoT workflow elements for CDL and IoT readiness
    * Additional interface configuration for an IoT broker server
    * Security policy allowing traffic between the IoT clients and broker
    
## IoT Traffic Generator Python Script

To be used in tandem with the HomeSkillet add-on configuration yet extensible to any
DHCP based deployed, the script is designed to:

    * Generate a set of IoT MAC addresses from a single Ubuntu server
    * DHCP interactions for each MAC address to create DHCP EAL log traffic
    * Create virtual MAC-IP interfaces on the Ubuntu server
    * Cycle MQTT client-broker traffic from each virtual MAC-IP interface
    
> The script requires root access and uses dhtest, intended to run on Linux platforms

