#!/bin/bash

# Group number
GROUPNUMBER=8
# Node configs
CONFIGDIR=frrouting_cfg
# boot script name
BOOT="boot"
# startup script name
STARTUP="start"
PREFIXBASE="fde4:8"
PREFIXLEN=32
# You can reuse the above two to generate ip addresses/routes, ...

# This function describes the network topology that we want to emulate
function mk_topo {
    echo "@@ Adding links and nodes"

%for router in range(len(data)):
%for inter in data[router]["interfaces"]:
%   if inter["virtual"] == "False":
%       if data[router]["id"]<inter["id"]:
    # ${data[router]["name"]} links to ${inter["name"]}
    add_link ${data[router]["name"]} ${inter["name"]}
%       endif
%   endif
%endfor
%endfor

    echo "@@Adding bridges nodes"
%for router in range(len(data)):
%for inter in data[router]["interfaces"]:
%   if inter["virtual"]=="True":

    bridge_node ${data[router]["name"]} ${inter["bridge"]} ${inter["interface"]}
%   endif
%endfor
%endfor

}

