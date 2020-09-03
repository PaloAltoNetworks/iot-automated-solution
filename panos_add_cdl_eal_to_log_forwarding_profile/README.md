# Add Cortex Data Lake (CDL) and Enhanced Application Logging (EAL) to Log Forwarding Profiles

After CDL is successfully enabled in the NGFW, this skillet simplifies the updates
needed to an existing log forwarding profile.

Skillet coverage includes:

    * capture the input name of the log forwarding profile
    * determine where the profile is configured (shared or vsys)
    * add CDL to existing log profile rules
    * enable EAL and create log profile rules for missing log types
    
> profile config file location is determined by how the profile is initially configured.
> The Web UI uses a local vsys model while the CLI adds the profile to a shared location.
> The CLI by default only shows the shared location profiles while the Web UI displays
> profiles stored in either location.

After the skillet is loaded and changes committed, ensure that CDL is active and connected
and the various log types are creating and forwarding logs to CDL.

```angular2
show logging-status
```

