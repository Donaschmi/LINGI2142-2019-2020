! -*- zebra -*-
!
! zebra configuration file
!
hostname ${data["name"]}
password zebra
enable password zebra
!
! Interface's description.
!
interface ${data["loopback"]["name"]}
    description loopback.
!
%for inter in data["interfaces"]:
%if inter["virtual"]=="False":
interface ${inter["interface"]}
description Link to ${inter["name"]}
%endif
!
%endfor
