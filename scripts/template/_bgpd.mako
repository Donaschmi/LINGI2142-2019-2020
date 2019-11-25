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
%if neigh["password"]!="none":
 neighbor ${neigh["ipv6"]} password ${neigh["password"]}
%endif
%endfor

address-family ipv6 unicast
 network fde4:8::/32
%for neigh in data["neighbors"]:
 neighbor ${neigh["ipv6"]} activate
%if data["next-hop"]=="True" and neigh["external"]=="False":
 neighbor ${neigh["ipv6"]} next-hop-self
%endif
%if neigh["rr"]=="True":
 neighbor ${neigh["ipv6"]} route-reflector-client
%endif
%endfor

%for neigh in data["neighbors"]:
 neighbor ${neigh["ipv6"]} update-source ${data["loopback"]["ipv6"]}
%endfor

exit-address-family
!
ip community-list 10 permit ${data["AS"]}:1000
ip community-list 11 permit ${data["AS"]}:1001
ip community-list 12 permit ${data["AS"]}:1005
ip community-list 13 permit ${data["AS"]}:2000
ip community-list 14 permit ${data["AS"]}:2100
ip community-list 15 permit ${data["AS"]}:2200
ip community-list 16 permit ${data["AS"]}:3000
!
%for policy in data["policies"]:
%if policy["type"] == "COMMUNITY":
declare community-list standard ${policy["link"]} permit ${policy["localpref"]}
%endif
%endfor
