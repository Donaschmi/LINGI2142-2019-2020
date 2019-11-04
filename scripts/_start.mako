#! /bin/sh
ldconfig
%for interface in data['interfaces']:
# Assigning IP addr for ${data['name']}-${interface['name']}
ip link set dev ${data['name']}-${interface['name']} up
ip -6 addr add ${interface['ipv6']}

%endfor

# zebra is required to make the link between all FRRouting daemons
# and the linux kernel routing table
LIBRARY_PATH=/usr/local/lib /usr/lib/frr/zebra -A 127.0.0.1 -f /etc/zebra.conf -z /tmp/${data['namemin']}.api -i /tmp/${data['namemin']}_zebra.pid &
# launching FRRouting OSPF daemon
LD_LIBRARY_PATH=/usr/local/lib /usr/lib/frr/ospf6d -f /etc/${data['namemin']}_ospf.conf -z /tmp/${data['namemin']}.api -i /tmp/${data['namemin']}_ospf6d.pid -A 127.0.0.1
