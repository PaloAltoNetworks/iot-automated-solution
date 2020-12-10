# Add Cortex Data Lake ready Log Forwarding Profile

This skillet configures a new log forwarding profile that is ready-to-go for Cortex 
Data Lake and Enhanced Application Logging.

> This profile is only configured for CDL and if syslog or other forwarding
> capabilities required, those must be added manually based on the user scenario.

Skillet operations includes:

    * capture the input name of the log forwarding profile
    * add log forwarding profile with all logs sent to Cortex Data Lake on vsys