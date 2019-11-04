! -*- zebra -*-
!
! zebra configuration file
!
hostname ${data['name']}
password zebra
enable password zebra
!
! Interface's description
!
interface lo
    description loopback.
!
%for interface in data['interfaces']
interface ${data['name']}-${interface['name']}
    description link to 
!
