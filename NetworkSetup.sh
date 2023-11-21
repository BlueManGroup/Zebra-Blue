#!/bin/bash

# Check for root privileges
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

# Update and install necessary packages
echo "Updating package list and installing necessary packages..."
sudo apt update
sudo apt install -y dnsmasq hostapd dhcpcd5 iptables

# Stop services to avoid conflicts during setup
echo "Stopping dnsmasq and hostapd services..."
sudo systemctl stop dnsmasq
sudo systemctl stop hostapd

# Step 5: Configure /etc/dhcpcd.conf for static IP of wlan0
echo "Configuring static IP for wlan0..."
echo "
interface wlan0
static ip_address=192.168.2.1/24
nohook wpa_supplicant
" | sudo tee -a /etc/dhcpcd.conf

# Restart dhcpcd
echo "Restarting dhcpcd..."
sudo service dhcpcd restart

# Step 6: Configure DHCP server (dnsmasq)
echo "Configuring dnsmasq..."
sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
echo "
interface=wlan0
dhcp-range=192.168.2.2,192.168.2.253,255.255.255.0,24h
" | sudo tee /etc/dnsmasq.conf

# Step 7: Configure the Access Point (hostapd)
echo "Configuring hostapd..."
echo "
interface=wlan0
driver=nl80211
ssid=ZebraBlue
hw_mode=g
channel=7
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=bluezebra
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
" | sudo tee /etc/hostapd/hostapd.conf

# Point to the hostapd configuration file
echo "DAEMON_CONF=\"/etc/hostapd/hostapd.conf\"" | sudo tee -a /etc/default/hostapd

# Step 8: Enable and start hostapd
echo "Enabling and starting hostapd..."
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
sudo systemctl start hostapd

# Step 9: Configure NAT
echo "Configuring NAT..."
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"

# Step 10: Enable IP forwarding
echo "Enabling IP forwarding..."
echo "net.ipv4.ip_forward=1" | sudo tee -a /etc/sysctl.conf
sudo sysctl -w net.ipv4.ip_forward=1

# Step 11: Reboot
echo "Setup complete. Rebooting now..."
sudo reboot

