! -*- bgp -*-
!
! BGP configuration file
!
hostname bgpd
password zebra
!
router bgp ${data["AS"]}
bgp router-id ${data["router-id"]}
no bgp default ipv4-unicast

%for neigh in data["neighbors"]:
neighbor ${neigh["ipv6"]} remote-as ${neigh["AS"]}

%if neigh["external"]==True:
neighbor ${neigh["ipv6"]} interface ${neigh["interface"]} 
%endif

%endfor

address-family ipv6 unicast

%for neigh in data["neighbors"]:
neighbor ${neigh["ipv6"]} activate
%if neigh["external"]==False:
neighbor ${neigh["ipv6"]} next-hop-self
%endif

neighbor ${neigh["ipv6"]} update-source ${data["loopback"]["ipv6"]}
%endfor


exit-address-family

