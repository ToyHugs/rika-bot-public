#!/bin/sh

# Enable IP forwarding
# sysctl -w net.ipv4.ip_forward=1

openvpn /vpn/vpnconfig.ovpn &

# sleep 10

# Allow all traffic to bypass the VPN
# Adjust the rules to suit your specific use case
# iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
# iptables -A FORWARD -i eth0 -o tun0 -j ACCEPT
# iptables -A FORWARD -i tun0 -o eth0 -m state --state RELATED,ESTABLISHED -j ACCEPT

# Keep the container running
tail -f /dev/null
