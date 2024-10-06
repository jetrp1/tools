#!/bin/bash

usage="./provision.py user@host vmid new_VMid [qm_commands]"

if (( $# < 3 )) ; then
    echo "Too few Arguments"
    echo "usage: $usage"
    exit 1
elif (( $# > 4)) ; then
    echo "Too Many Arguments"
    echo "usage: $usage"
    exit 1
fi

ssh_info=$1
old_vmid=$2
new_VMid=$3
qm_commands=$4

# Verify SSH Login info
loginResult=$(ssh $ssh_info id)

if [ $? == 255 ] ; then 
    echo "SSH Connection Error, Please validate ssh credentials"
    exit 1
fi

# Implement confirming QM Status
qm_status=$(ssh $ssh_info qm config $old_vmid)

if [ $? != 0 ] ; then 
    echo "Error getting QM Status"
    exit 1
fi

template_status=$(ssh $ssh_info qm config $old_vmid | awk '/template:/ {print $2}')

if [ "$template_status" != "1" ] ; then 
    echo "VM $old_vmid is not a template"
    exit 1
fi

ssh $ssh_info qm clone $old_vmid $new_VMid $qm_commands --full

# TODO: Add fancy progress bar for the drive copy

exit 0