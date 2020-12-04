# Add IoT-Ready Tap Mode Deployment to NGFW

#### Prerequisites 
Cortex Data Lake (CDL) and Enhanced Application Logging (EALs) must already be enabled
on the firewall before running this configuration skillet.

#### This Skillet Configurations
Given an ethernet interface as an input, the skillet will:

1. Configure the ethernet interface in tap mode
2. Create a tap zone
3. Create Alert-All security profiles according to Iron-Skillet
4. Create Alert-All security group
5. Create a CDL- and EAL-ready log forwarding profile
6. Create a security rule to allow, alert on, and forward all traffic seen from 
the tap interface
