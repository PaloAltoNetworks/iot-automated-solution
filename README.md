# IoT Automated Solutions

Collection of content to help automate NGFW Cortex IoT deployments, configuration, and
traffic generation

## Prerequisites

    * Cortex Data Lake license activated, preferably in the Customer Support Portal 
    * Cortex Data Lake NGFW onboarding Pre-Shared Key generated/captured
    * NGFW serial number activated for Cortex IoT
    * panHandler: import the Github repo panos-logging-skillets
    * panHandler 4.0 or later if used to play skillets and playbooks

## IoT Configuration Workflow


Working in tandem with the content in 
[panos-logging-skillets](https://github.com/PaloAltoNetworks/panos-logging-skillets)
to help simplify NGFW IoT configuration.

The workflow provides a simple web form menu to select elements for Cortex Data Lake
and IoT readiness including:

    * Cortex Data Lake (CDL) implementation Ansible playbook
    * Update log-forwarding profiles with CDL and Enhancement Application logging. 
    * For 10.x NGFW DHCP servers, enable DHCP session broadcast
    * For pre-10.x NGFW DHCP servers, convert to a logic interface server and DHCP relay
    * Add a DHCP security policy for visbility
    * Configuration/system validation checks for CDL and IoT configuration elements
    
For more details about which options to choose in the workflow, navigate to the **README** in the 
`workflow_iot_setup` directory.

For more details about each element in the IoT Configuration workflow, navigate to the according
subdirectory to view additional **README**s. 
    
### IoT Configuration Skillets

Simple configuration skillets designed to update the NGFW configuration to be CDL/IoT ready
and are used by the above IoT Configuration Workflow.

#### IoT Tap-Based Sensor Configuration Skillet

After CDL is successfully enabled in the NGFW, this workflow gives the option to turn the NGFW into a tap-based 
sensor to gain visibility into the IoT devices and IoT traffic traversing a network.

    * Add tap-based network components to NGFW
    * Create profile to forward EAL and other logs to CDL
    * Configure IronSkillet security profiles and groups
    * Add security rule to allow, alert on, and forward all traffic seen from the tap interface

### IoT Validation Skillet

Validate key CDL and IoT NGFW elements to help users discover missing elements
required for IoT readiness. Used by the above IoT Configuration Workflow.

## IoT POC built using HomeSkillet Add-on Configuration

Augment the HomeSkillet configuration for an IoT configuration and PoC.

    * Leverage the IoT workflow elements for CDL and IoT readiness
    * Additional L3 interface configuration for an IoT broker server
    * Security policy allowing traffic between the IoT clients and broker
    
## IoT Traffic Generator Python Script

To be used in tandem with the HomeSkillet add-on configuration yet extensible to any
DHCP based deployed, the script is designed to:

    * Generate a set of IoT MAC addresses from a single Ubuntu server
    * DHCP interactions for each MAC address to create DHCP EAL log traffic
    * Create virtual MAC-IP interfaces on the Ubuntu server
    * Cycle MQTT client-broker traffic from each virtual MAC-IP interface
    
> The script requires root access and uses dhtest, intended to run on Linux platforms


## Support Policy
The code and templates in the repo are released under an as-is, best effort,
support policy. These scripts should be seen as community supported and
Palo Alto Networks will contribute our expertise as and when possible.
We do not provide technical support or help in using or troubleshooting the
components of the project through our normal support options such as
Palo Alto Networks support teams, or ASC (Authorized Support Centers)
partners and backline support options. The underlying product used
(the VM-Series firewall) by the scripts or templates are still supported,
but the support is only for the product functionality and not for help in
deploying or using the template or script itself. Unless explicitly tagged,
all projects or work posted in our GitHub repository
(at https://github.com/PaloAltoNetworks) or sites other than our official
Downloads page on https://support.paloaltonetworks.com are provided under
the best effort policy.

## Related Links
To learn more about how to use the CDL logging skillets and what exactly each one does, please refer to the following link:
[PAN-OS CDL Logging](https://live.paloaltonetworks.com/t5/quickplay-solutions-articles/pan-os-cortex-data-lake-logging-quickplays/ta-p/348669)

For a more in depth look at the requirements and flow of the IoT automated solution please refer to the following link:
[IoT Automated Solutions Collection](https://gallery.pan.dev/repo/iot-automated-solution)
