#!/bin/bash

ipv4_dns="$1"
ipv6_dns="$2"

uuids=$(nmcli -g UUID connection show)

for uuid in $uuids; do
    nmcli connection modify "$uuid" ipv4.dns "$ipv4_dns"
    nmcli connection modify "$uuid" ipv6.dns "$ipv6_dns"
    nmcli connection modify "$uuid" ipv4.ignore-auto-dns yes
    nmcli connection modify "$uuid" ipv6.ignore-auto-dns yes
done

systemctl restart NetworkManager