!
! OSPF configuration for ${data['id']}
!
hostname ${data['name']}
password zebra
log stdout
service advanced-vty
!
debug ospf6 neighbor state
!
interface lo
    ipv6 ospf6 cost 5
    ipv6 ospf6 hello-interval 10
    ivp6 ospf6 dead-interval 40
    ipv6 ospf6 instance-id 0

%for interface in data['interfaces']:
interface ${data['name']}-name
    ipv6 ospf6 cost 5
    ipv6 ospf6 hello-interval 10
    ipv6 ospf6 dead-interval 40
    ipv6 ospf6 instance-id 0
!
%endfor
router ospf6
    ospf6 router-id 100.251.23.***
    area 0.0.0.0 range fde4:8:0::***/64
    %for interface
    interface lo area 0.0.0.0
!
