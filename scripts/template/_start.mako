#! /bin/sh
ldconfig

# Assigning IP addr for ${data["loopback"]["name"]}
ip link set dev ${data["loopback"]["name"]} up
ip -6 addr add ${data["loopback"]["ipv6"]} dev ${data["loopback"]["name"]}

%for inter in data["interfaces"]:
# Assigning IP addr for ${inter["interface"]}
ip link set dev ${inter["interface"]} up
ip -6 addr add ${inter["ipv6"]} dev ${inter["interface"]}
%endfor

# zebra is required to make the link between all FRRouting daemons
# and the linux kernel routing table
LIBRARY_PATH=/usr/local/lib /usr/lib/frr/zebra -A 127.0.0.1 -f /etc/zebra.conf -z /tmp/${data["namemin"]}.api -i /tmp/${data["namemin"]}_zebra.pid &
# launching FRRouting OSPF daemon
LD_LIBRARY_PATH=/usr/local/lib /usr/lib/frr/ospf6d -f /etc/${data["namemin"]}_ospf.conf -z /tmp/${data["namemin"]}.api -i /tmp/${data["namemin"]}_ospf6d.pid -A 127.0.0.1 &
#launching FFRouting BGP daemon
LD_LIBRARY_PATH=/usr/local/lib /usr/lib/frr/bgpd -f /etc/${data["namemin"]}_bgpd.conf -z /tmp/${data["namemin"]}.api -i /tmp/${data["namemin"]}_bgpd.pid -A 127.0.0.1 &
