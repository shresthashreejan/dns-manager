#!/bin/bash

uuids=$(nmcli -g UUID connection show)
ipv4_dns="9.9.9.9 149.112.112.112"
ipv6_dns="2620:fe::fe 2620:fe::9"

for uuid in $uuids; do
    nmcli connection modify "$uuid" ipv4.dns "$ipv4_dns"
    nmcli connection modify "$uuid" ipv6.dns "$ipv6_dns"
    echo "Quad9 DNS servers set for connection with UUID: $uuid"
done