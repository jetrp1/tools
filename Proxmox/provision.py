#!/bin/env python3

import subprocess as sp
import proxmoxer



if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser(prog="provision.py")
    parser.add_argument('user', help='User account on the proxmox Server')
    parser.add_argument('host', help='Proxmox host')
    parser.add_argument('vmid', help='The VM id of the VM to clone')
#    parser.add_argument('[OPTIONS]', help='The Arguments passed to qm clone command')
    parser.add_argument('-s', '--start', action='store_true', help='Starts the VMs after creation')
    parser.add_argument('newHosts', nargs='*', help='The VM id of the new VM')
    args = parser.parse_args()


    prox = proxmoxer


# Steps
# Verify SSH credentials 
# Verify VM is Valid
# - VM exists
# - Is Cloneable




'''
My Vision for this script

as input:
    a vitualiztion host (proxmox only for now)
    a list of VM hostname
    available IP address range

the script connects to the specific virtualization server
creates the requested VMs
    - full clones of specified template
    - should i add ability to create without template?
makes DHCP reservations for each VM
starts each VM - if requested
returns any errors
returns the relevant VM info one per line: 
    <hostname> <vmid> <vm ip address>

Should i make it possible to run a script against each vm?

    
'''