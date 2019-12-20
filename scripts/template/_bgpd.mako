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

!

%for neigh in data["neighbors"]:
neighbor ${neigh["ipv6"]} remote-as ${neigh["AS"]}
%if neigh["external"]==True:
neighbor ${neigh["ipv6"]} interface ${neigh["interface"]} 
%endif
%if neigh["password"]!="none":
 neighbor ${neigh["ipv6"]} password ${neigh["password"]}
%endif

%endfor

!

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
%if "route-map-in" in neigh:
  neighbor ${neigh["ipv6"]} route-map ${neigh["route-map-in"]} in
%endif
%if "route-map-out" in neigh:
  neighbor ${neigh["ipv6"]} route-map ${neigh["route-map-out"]} out
%endif
%if "prefix-list-in" in neigh:
  neighbor ${neigh["ipv6"]} prefix-list ${neigh["prefix-list-in"]} in
%endif
%if "prefix-list-out" in neigh:
  neighbor ${neigh["ipv6"]} prefix-list ${neigh["prefix-list-out"]} out
%endif

%endfor

%for neigh in data["neighbors"]:
 neighbor ${neigh["ipv6"]} update-source ${data["loopback"]["ipv6"]}
%endfor

exit-address-family

!

%for policy in data["policies"]:
%if policy["type"] == "COMMUNITY-LIST":
bgp community-list ${policy["setting"]} ${policy["name"]} permit ${policy["value"]}
%endif
%endfor

!

%for policy in data["policies"]:
%if policy["type"] == "EXPORT-FILTER":
ipv6 prefix-list ${policy["name"]} permit ${policy["ipv6"]}
%endif
%endfor

!

%for policy in data["policies"]:
%if policy["type"] == "ROUTE-MAP":
%   if "first" in policy:
route-map ${policy["name"]} permit ${policy["first"]}
%       if "first_pol" in policy:
%           for line in policy["first_pol"]:
    ${line}
%           endfor
%       endif
%       if "second" in policy:
route-map ${policy["name"]} permit ${policy["second"]}
%           if "second_pol" in policy:
%               for line in policy["second_pol"]:
    ${line}
%               endfor
%           endif
%               if "third" in policy:
route-map ${policy["name"]} permit ${policy["third"]}
%               endif
%       endif
%   endif
!
%endif
%endfor
