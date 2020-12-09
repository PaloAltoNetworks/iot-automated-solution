# Enable Device Identification per Zone

> **ONLY for firewalls running PAN-OS 10.x and above**

This skillet is used to enable Device-ID on specified zones in order to identify 
devices, obtain policy rule recommendations for those devices, and enforce Security
policies based on these recommendations.

>As a best practice, you never should enable Device-ID for a zone that contains the internet.

Skillet operations includes:

    * populates the web UI with the existing zones 
    * capture the input name(s) of the zones to configure
    * enable Device-ID on each inputted zone

> The `iot_get_device_values` skillet (located in the *rest_get_device_values* directory)
> must be run with this skillet to capture the existing zones. This is easily done in 
> the IoT workflow.


