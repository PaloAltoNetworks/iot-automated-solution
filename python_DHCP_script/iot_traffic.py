#!/usr/bin/python3
# Copyright (c) 2018, Palo Alto Networks
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

# Author: Bora MutluoGlu <bmutluoglu@paloaltonetworks.com>
# Author: Scott Shoaf <sshoaf@paloaltonetworks.com>

'''
Palo Alto Networks IoT POC Traffic Generator

Use input MAC addresses to source DHCP interactions and obtain IP addresses.
DHCP traffic is logged by FW as an EAL and sent to CDL and the IoT application.
IP addresses are captured to create logical interfaces on the IoT client host.
Lastly paho MQTT sessions are generated between an MQTT client and broker
MQTT traffic is logged by FW and sent to CDL and the IoT application.

This software is provided without support, warranty, or guarantee.
Use at your own risk.
'''

from subprocess import PIPE, Popen
from subprocess import check_output

import click
import paho.mqtt.client as mqtt
from scapy.all import time, random


def generate_macs(num_to_gen, mac_oui, mac_4_5_octets):
    """
    generate a deterministic list of mac addresses to minimize total number of
    clients seen by Cortex IoT Guardian
    :param num_to_gen: how many macs to generate
    :param mac_oui: vendor portion of mac address
    :param mac_4_5_octets: 4th and 5th octets so only 6th octet changes
    :return: mac_list - list of num_to_gen length of MAC addresses
    """
    mac_prefix = f'{mac_oui}:{mac_4_5_octets}'
    mac_list = []

    for x in range(0, num_to_gen):
        # generate hex value as 6th octet value for each mac address
        # using the sequence value will keep deterministic vs a random mac address
        # the if conditional is used to prepend a zero if x hex value is single digit
        mac_6th = hex(x).split('x')[1]
        if len(mac_6th) == 1:
            mac_list.append(f'{mac_prefix}:0{mac_6th}')
        else:
            mac_list.append(f'{mac_prefix}:{mac_6th}')

    return mac_list


def get_dhcp_ip(mac_list, client_intf):
    """
    dhcp method to get an IP address for each MAC address
    :param mac_list: list of mac addresses
    :param client_intf: string for Client interface connected to NGFW
    :return: mac_ip_dict - dictionary of MAC address to associated IP address
    """
    mac_ip_dict = {}
    for mac in mac_list:
        out = check_output(f'sudo ./dhtest/dhtest -i {client_intf} -m {mac}', shell=True)
        print(out.decode('ascii'))
        mac_ip_dict[mac] = out.decode('ascii').split("Acquired IP: ", 1)[1].rstrip("\n")

    return mac_ip_dict


def create_logical_intf(mac_ip_dict, client_intf):
    """
    use the DHCP MAC-IP mappings to create MACVLAN bridge interfaces on the client
    :param mac_ip_dict: MAC-IP mapping dict
    :param client_intf: string for Client interface connected to NGFW
    :return: void
    """

    for mac in mac_ip_dict:
        # Grab IP 4th octet to use as interface label
        label_suffix = mac_ip_dict[mac].split('.')[3]
        intf_label = f'iot{label_suffix}'

        print(f'creating interface {intf_label} for MAC {mac} and IP {mac_ip_dict[mac]}')

        # Create logical MACVLAN interface
        add_if = Popen(f'sudo ip link add {intf_label} link {client_intf} type macvlan mode bridge',
                       shell=True, stdout=PIPE, stderr=PIPE)
        stdout, stderr = add_if.communicate()

        # Assign MAC address to new interface
        add_mac = Popen(f'sudo ip link set {intf_label} address {mac}',
                        shell=True, stdout=PIPE, stderr=PIPE)
        stdout, stderr = add_mac.communicate()

        # Add IP address to new MACVLAN interface
        add_ip = Popen(f'sudo ip addr add {mac_ip_dict[mac]} dev {intf_label}',
                       shell=True, stdout=PIPE, stderr=PIPE)
        stdout, stderr = add_ip.communicate()

        # Bring up MACVLAN interface
        bring_up = Popen(f'sudo ifconfig {intf_label} up',
                         shell=True, stdout=PIPE, stderr=PIPE)
        stdout, stderr = bring_up.communicate()


def iot_traffic(mapping_dict, broker_address):
    """
    Connect, publish, disconnect mqtt traffic
    :param iot_mac_ip: MAC-IP mapping dictionary
    :param broker_address: IP address of MQTT broker
    :return: void
    """

    while True:
        for mac in mapping_dict:
            # Create new MQTT client instance
            client = mqtt.Client(mac)
            client.reinitialise()

            # MQTT callback information
            client.on_message = on_message
            client.on_connect = on_connect
            client.on_disconnect = on_disconnect
            client.on_publish = on_publish
            client.on_log = on_log

            print(f'\nconnecting {mapping_dict[mac]} to broker {broker_address}')

            # Client connects to the broker and waits to ensure connection completes
            client.connect(broker_address, port=1883, bind_address=mapping_dict[mac])  # connect to broker
            time.sleep(5)

            # Start traffic loop in background thread while publishing info to broker
            client.loop_start()
            client.subscribe("Security/Monitor")
            randval = random.randint(1000, 9999)  # random value to use in publish message
            client.publish("Security/Monitor", randval)
            time.sleep(5)
            client.publish("security/secops/event", randval)
            client.loop_stop()

            # Disconnect MQTT connection from broker
            # client.disconnect()

        # Delayed response
        time.sleep(30)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    # topic = msg.topic
    m_decode = str(msg.payload.decode("utf-8", "ignore"))
    print("Message received=" + m_decode)


# The callback for when the client receives a CONNACK response from the broker.
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected Ok")
    else:
        print("Connection failed code= ", rc)


# The callback for when the client disconnects from the broker.
def on_disconnect(client, userdata, flags, rc=0):
    print("Disconnected with code= " + str(rc))


# The callback for when the publish message was transmitted completely to the broker.
def on_publish(client, userdata, result):
    print("data published \n")
    pass


# The callback for when the client has log information.def on_log(client, userdata, level, buf):
def on_log(client, userdata, level, buf):
    print("log " + buf)


@click.command()
@click.option("-b", "--broker_address", help="IP address of the IoT MQTT broker)", type=str, default="172.31.0.68")
@click.option("-m", "--mac_oui", help="Virtual clients' MAC OUI", type=str, default="AC:64:17")
@click.option("-o", "--mac_4_5_octets", help="Virtual clients' MAC 4th and 5th octets", type=str, default="AB:CD")
@click.option("-n", "--num_macs", help="Number of MAC addresses/clients to generate", type=int, default=5)
@click.option("-i", "--client_intf", help="Client interface connected to NGFW", type=str, default='ens4')
def cli(broker_address, mac_oui, mac_4_5_octets, num_macs, client_intf):
    """
    DHCP and MQTT traffic generator
    """

    print('_' * 60)
    print(f'\ncreating {num_macs} MAC addresses with OUI {mac_oui}')
    print(f'MQTT traffic will be sent to broker IP {broker_address}')
    print('_' * 60)

    # Generate list of MAC address as input to DHCP method
    mac_list = generate_macs(num_macs, mac_oui, mac_4_5_octets)
    print('\nusing MAC addresses:')
    print(f'{mac_list}\n')

    # DHCP method to get IP addresses for each MAC address
    iot_mac_ip = get_dhcp_ip(mac_list, client_intf)
    # print(iot_mac_ip)

    # Create IoT client logical interfaces for MQTT sessions used to connect to broker
    create_logical_intf(iot_mac_ip, client_intf)

    # MQTT publish sessions between client and broker for each mac-ip entry
    iot_traffic(iot_mac_ip, broker_address)


if __name__ == '__main__':
    cli()
