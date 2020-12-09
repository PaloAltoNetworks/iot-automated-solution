# Add Logging to Existing Security Rules

This skillet allows the user to select existing security rules to attach a log forwarding
profile to.

Skillet operations includes:

    * populates the web UI with the existing security rules 
    * populates the web UI with the existing log forwarding profile
    * capture the input name(s) of the rules to configure
    * attaches the log forwarding profile to the rule(s)

> The `iot_get_device_values` skillet (located in the *rest_get_device_values* directory)
> must be run with this skillet to capture the existing zones. This is easily done in 
> the IoT workflow.