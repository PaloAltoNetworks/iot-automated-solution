# Initial Firewall setup
For the script and topology to properly work you need to first
set up your firewall correctly. The following steps will guide
you through this process.

* Use HomeSkillet 10.0 L3 mode to load base firewall configuration(Security, Network and Zones, IronSkillet)
* Run the CDL playbook to connect firewall for CDL logging
* Run CDL/EAL profile Skillet to update all profiles for logging
* Add Security Policies to firewall via Homeskillet add-ons skillet
* Turn off zone protect profiles

# Setting up Client side Linuxbox
You want to map your Client address to match the NGFW interface address.
You also need to set up your routing table to allow the Client to route to remote
networks. This section will walk you through that process. You will be using Paho to
connect to the Broker and publish messages(Paho-MQTT)

* Add a network end to broker 
* View the arp/rp filter current states via ```sysctl -ar 'rp_filter'```
* Need to change current states of filters via these commands
    + ```sudo sysctl -w 'net.ipv4.conf.all.arp_ignore=1'```
    + ```sudo sysctl -w 'net.ipv4.conf.all.arp_announce=2'```
    + ```sudo sysctl -w 'net.ipv4.conf.all.rp_filter=2'```
* Alter routing table to be able to reach remote networks
    + ```netstat -rn```
    + ```sudo ip route add {remote network IP} via {current routing gateway IP} dev {Linux interface}```


# Setting up Broker side Linuxbox
You need to install MQTT on the broker side in order to have the
Client publish messages and subscribe to topics. You also need to
alter the routing table of the Broker to be able to route to remote
networks.

* Install MQTT on the Broker side
* Alter routing table to be able to reach remote networks
    + ```netstat -rn```
    + ```sudo ip route add {remote network IP} via {current routing gateway IP} dev {Linux interface}```


# Running the IoT traffic generator
Requires Linux host such as Ubuntu to run

Prior to running the script be sure to do ``` make ```  
within the dhtest directory found on the Client side.

The command to run the traffic generation script is

`sudo python3 iot_traffic.py`

