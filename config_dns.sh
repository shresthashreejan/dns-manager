#!/bin/bash

ipv4_dns="$1"
ipv6_dns="$2"

uuids=$(nmcli -g UUID connection show)

for uuid in $uuids; do
    nmcli connection modify "$uuid" ipv4.dns "$ipv4_dns"
    nmcli connection modify "$uuid" ipv6.dns "$ipv6_dns"
    echo "Quad9 DNS servers set for connection with UUID: $uuid"
done

systemctl restart NetworkManager