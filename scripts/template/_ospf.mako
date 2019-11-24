!
! OSPF configuration for ${data["name"]}
!
hostname ${data["name"]}
password zebra
log stdout
service advanced-vty
!
debug ospf6 neighbor state
!
interface ${data["loopback"]["name"]}
    ipv6 ospf6 cost 5
    ipv6 ospf6 hello-interval 10
    ipv6 ospf6 dead-interval 40
    ipv6 ospf6 instance-id 0
!
%for inter in data["interfaces"]:
interface ${inter["interface"]}
    ipv6 ospf6 cost 5
    ipv6 ospf6 hello-interval 10
    ipv6 ospf6 dead-interval 40
    ipv6 ospf6 instance-id 0
!
%endfor
router ospf6
    ospf6 router-id 100.251.23.${data["id"]}
%for inter in data["interfaces"]:
%if inter["virtual"]=="False":
    interface ${inter["interface"]} area ${data["area"]}
%endif
%endfor
    interface ${data["loopback"]["name"]} area ${data["area"]}
!
