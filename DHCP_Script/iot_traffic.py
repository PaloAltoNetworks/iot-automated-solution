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

Use input MAC addresses to source DHCP interactions and obtain IP addresses
DHCP traffic is logged to CDL and the IoT application
IP addresses are captured to create logical interfaces on the IoT client host
Lastly paho MQTT sessions are generated between an MQTT client and broker

This software is provided without support, warranty, or guarantee.
Use at your own risk.
'''

import click
import json
import os
import paho.mqtt.client as mqtt  # import the client1
import random
import time  # For sleep function delays
from distutils import text_file
from scapy.all import *
from scapy.layers.dhcp import BOOTP, DHCP
from scapy.layers.inet import UDP, IP
from scapy.layers.l2 import Ether
from subprocess import PIPE, Popen
from subprocess import check_output


def generate_macs(num_to_gen, mac_oui, mac_4_5_octets):
    """
    generate a deterministic list of mac addresses
    :param num_to_gen: how many macs to generate
    :param mac_oui: vendor portion of mac address
    :param mac_4_5_octets: 4th and 5th octets so only 6th octet changes
    :return: mac_list
    """

    mac_prefix = f'{mac_oui}:{mac_4_5_octets}'
    mac_list = []

    for x in range(0, num_to_gen):
        # generate hex value as 6th octet value for each mac address
        # using the sequence value will keep deterministic vs a random mac address
        # if conditional is used to prepend a zero if x hex value is single digit
        mac_6th = hex(x).split('x')[1]
        if len(mac_6th) == 1:
            mac_list.append(f'{mac_prefix}:0{mac_6th}')
        else:
            mac_list.append(f'{mac_prefix}:{mac_6th}')

    return mac_list


def get_dhcp_ip(mac_list, client_intf):
    """
    dhcp method to get an IP address for each MAC address
    :param mac_list: input list of mac addresses
    :return: mac_ip_dict
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
    :return:
    """

    for mac in mac_ip_dict:
        # grab IP 4th octet to use as interface label
        label_suffix = mac_ip_dict[mac].split('.')[3]
        intf_label = f'iot{label_suffix}'

        print(f'creating interface {intf_label} for MAC {mac} and IP {mac_ip_dict[mac]}')

        # create logical macvlan interface
        add_if = Popen(f'sudo ip link add {intf_label} link {client_intf} type macvlan mode bridge',
                       shell=True, stdout=PIPE, stderr=PIPE)
        stdout, stderr = add_if.communicate()

        # assign mac address to new interface
        add_mac = Popen(f'sudo ip link set {intf_label} address {mac}',
                        shell=True, stdout=PIPE, stderr=PIPE)
        stdout, stderr = add_mac.communicate()

        # add ip address to new macvlan interface
        add_ip = Popen(f'sudo ip addr add {mac_ip_dict[mac]} dev {intf_label}',
                       shell=True, stdout=PIPE, stderr=PIPE)
        stdout, stderr = add_ip.communicate()

        # bring up interface
        bring_up = Popen(f'sudo ifconfig {intf_label} up',
                         shell=True, stdout=PIPE, stderr=PIPE)
        stdout, stderr = bring_up.communicate()



def iot_traffic(mapping_dict, broker_address):
    """
    connect, publish, disconnect mqtt traffic
    :param iot_mac_ip: mac-ip mapping dictionary
    :param broker_address: ip address of mqtt broker
    :return:
    """

    while True:

        for mac in mapping_dict:

            client = mqtt.Client(mac)  # create new  client instance
            client.reinitialise()

            # callback information
            client.on_message = on_message
            client.on_connect = on_connect
            client.on_disconnect = on_disconnect
            client.on_publish = on_publish
            client.on_log = on_log

            print(f'\nconnecting {mapping_dict[mac]} to broker {broker_address}')

            # connect, publish, disconnect stages
            client.connect(broker_address, port=1883, bind_address=mapping_dict[mac])  # connect to broker
            time.sleep(5) # making sure connection completes
            client.loop_start()  # start loop
            client.subscribe("Security/Monitor")
            randval = random.randint(1000, 9999)  # random value to use in publish message
            client.publish("Security/Monitor", randval)  # publish
            time.sleep(5) # delay after publish
            client.publish("security/secops/event", randval)
            client.loop_stop()  # stop loop

            #client.disconnect()  # disconnect from broker


        time.sleep(30)  # delayed response


# callback functions
def on_log(client, userdata, level, buf):
    print("log " + buf)

# logging callback function allows us to get logging information upon connect

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected Ok")
    else:
        print("Connection failed code= ", rc)


# connect callback function gives us information on when we connect

def on_disconnect(client, userdata, flags, rc=0):
    print("Disconnected with code= " + str(rc))


def on_message(client, userdata, msg):
    topic = msg.topic
    m_decode = str(msg.payload.decode("utf-8", "ignore"))
    print("Message received=" + m_decode)

def on_publish(client,userdata,result):   #create function for callback
    print("data published \n")
    pass

@click.command()
@click.option("-b", "--broker_address", help="IP address of the IoT MQTT broker)", type=str, default="172.31.0.68")
@click.option("-m", "--mac_oui", help="virtual client MAC OUI", type=str, default="AC:64:17")
@click.option("-o", "--mac_4_5_octets", help="MAC 4th and 5th octets", type=str, default="AB:CD")
@click.option("-n", "--num_macs", help="number of MAC addresses to generate", type=int, default=5)
@click.option("-i", "--client_intf", help="client interface connected to NGFW", type=str, default='ens4')
def cli(broker_address, mac_oui, mac_4_5_octets, num_macs, client_intf):
    """
    DHCP and MQTT traffic generator
    """

    print('_' * 60)
    print(f'\ncreating {num_macs} MAC addresses with OUI {mac_oui}')
    print(f'MQTT traffic will be sent to broker IP {broker_address}')
    print('_' * 60)

    # generate list of MAC address as input to DHCP method
    mac_list = generate_macs(num_macs, mac_oui, mac_4_5_octets)
    print('\nusing MAC addresses:')
    print(f'{mac_list}\n')

    # DHCP method to get IP addresses for each MAC address
    iot_mac_ip = get_dhcp_ip(mac_list, client_intf)
    #print(iot_mac_ip)

    # create IoT client logical interfaces for MQTT sessions
    create_logical_intf(iot_mac_ip, client_intf)

    # mqtt publish sessions for each mac-ip entry
    iot_traffic(iot_mac_ip, broker_address)

if __name__ == '__main__':
    cli()