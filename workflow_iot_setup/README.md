# IoT Configuration Workflow

This workflow is used as the starting point for the IoT automation.

Core items include:

    * Configuration and system state assessment for IoT
    * Cortex Data Lake (CDL) and Enhanced Application Logging (EAL) activation and configuration
    * NGFW topology-specific DHCP configuration

> **Assumption**: The automation is run on an existing, licensed firewall with updated interfaces, 
> zones, and pre-IoT policies already in place. 

## Automation Element 1 - IoT-Readiness Validations

This workflow gives the option to run the IoT validation skillet to determine if the NGFW is
correctly configured for IoT. These validation checks can be run at the beginning of the 
workflow to discover which configuration changes need to occur on the brown-field NGFWs and/or 
at the end of the workflow to verify IoT readiness.  

## Automation Element 2 - Cortex Data Lake (CDL) and Enhanced Application Logging Enablement

Then, the workflow gives the options necessary to enable logging services on the NGFW and
to configure log traffic to be sent to CDL. These steps are necessary for the IoT instance
to properly receive device traffic. 

These questions about the current state of the NGFW determine which automation options to select:

    1. Is CDL enabled on the NGFW?
    2. Are logs currently sent to Panorama and will need to be duplicated for both Panorama and CDL?
    3. Can an existing log forwarding profile be updated to send to CDL, or 
        is there a need for a new CDL- and EAL-enabled log forwarding profile?
    4. Is there a need to update a current security rules to use the log profile?

Depending on the answer to these questions, the following options are available:

    * Activate and configure CDL on the NGFW
    * Enable Duplicate Logging 
    * Enable CDL and EAL on an existing log-forwarding profile
    * Create a new log forwarding profile with CDL and EAL enabled
    * Update security rules with the CDL- and EAL-enabled log forwarding profile

## Automation Element 3 - Topology-Specific IoT Readiness Options

Once Cortex Data Lake and Enhanced Application Logging are configured, some topology-specific
configurations may need to occur in order for the firewall to see necessary IoT traffic, including
DHCP unicast packets. 

These questions about the current state of the NGFW determine which automation options to select:

    1. What PAN-OS release is the NGFW running?
    2. Is a DHCP server configured on an interface of the NGFW?
    3. Is the IoT/DHCP traffic visible across a virtual wire?

Depending on the answers to the first question, there are varying options listed in the following sections.

### 10.x release and later options 

Based on 10.x dropdown selection, the user has these options:

    * Enable Device-ID on the IoT traffic source zone to increase visibility and allow for policy enforcement
    * If the answer to question #2 is yes, enable DHCP Broadcast Session 
    * If the answer to question #3 is yes, enable Multicast Firewalling

### 9.x release options

Based on 9.x dropdown selection, the user has these options:

    * If the answer to question #2 is yes, convert the DHCP server to a DHCP relay
    * If the answer to question #3 is yes, enable Multicast Firewalling

## Special Case - Configure tap-based sensor elements to capture log events

This workflow gives the option to turn the NGFW into a tap-based sensor to gain visibility into the IoT
devices and IoT traffic traversing a network. By clicking _Yes_ to the **Special Case** radio button, the 
automation will create brand-new configuration elements on the NGFW. 

In addition to clicking _Yes_, Cortex Data Lake must be activated and 
configured. 

The only other configuration option that potentially needs to be run at the same time as the tap-based sensor
configuration is the _Enable Device-ID on a source zone_ for PAN-OS 10.x NGFWs.