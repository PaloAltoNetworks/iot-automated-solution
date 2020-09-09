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
Palo Alto Networks IoT POC Interface Clean Up

deletes the iotXX interfaces from the local host

This software is provided without support, warranty, or guarantee.
Use at your own risk.
'''

from subprocess import PIPE, Popen

import click
import netifaces


def delete_logical_intf(intf_list, prefix_str):
    """
    for interfaces match the prefix string, delete the interface
    :param intf_list: list of host interfaces
    :param prefix_str: prefix string of interest
    :return:
    """

    for interface in intf_list:
        deletables = []
        # interface the interfaces looking for one matching the prefix string
        # then delete that interface
        if prefix_str in interface:
            print(interface)

            print(f'deleting interface {interface}')

            # delete interface
            add_if = Popen(f'sudo ip link delete {interface}', shell=True, stdout=PIPE, stderr=PIPE)
            stdout, stderr = add_if.communicate()

            deletables.append(interface)

    # courtesy message that no interfaces were found matching the prefix_str
    if not deletables:
        print(f'\nno interfaces starting with {prefix_str} were found\n')


@click.command()
@click.option("-p", "--prefix_str", help="prefix string for interfaces to be removed", type=str, default="iot")
def cli(prefix_str):
    """
    delete interfaces
    """

    print('_' * 60)
    print(f'\ndelete host interfaces starting with {prefix_str}')
    print('_' * 60)

    # get all interfaces starting with the prefix string
    # print (netifaces.interfaces())
    interfaces = netifaces.interfaces()

    # delete interfaces
    delete_logical_intf(interfaces, prefix_str)


if __name__ == '__main__':
    cli()
