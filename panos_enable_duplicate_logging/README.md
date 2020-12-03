# Enable Duplicate Logging

If a firewall is already configured to send to Panorama, then duplicate logging
should be enabled to send logs to both Panorama and Cortex Data Lake. This is used
for customer evaluations -- the customer will not have a 30-60 day gap in their
logs when the eval Cortex Data Lake instance is destroyed.