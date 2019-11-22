#!/bin/bash

# Create a virtual network using network namespaces and veth pairs
# to connect them.
# Assuming $CONFIGDIR == "cfg":
# * Files in cfg/<Node name> will be overlaid over /etc, i.e. if a file with
# the same name exists in both directory, the one in cfg/<Node name> will
# be the one used.
# * If cfg/<Node name>_$BOOT (defaults to cfg/<Node name>_boot) exists and
# is executable, it will be executed when the node is created
# * If cfg/<Node name>_$STARTUP (defaults to cfg/<Node name>_start) exists and
# is executable, it will be executed when the whole network has started
#

# IMPORTANT NOTE: Node names MUST NOT exceed 9 characters.
# This is due to the limitation to 14 characters of interface names

# You can override any of these settings on a per-topology basis
# Group number
GROUPNUMBER=8
# Node configs
CONFIGDIR=frrouting_cfg
# boot script name
BOOT="boot"
# startup script name
STARTUP="start"
PREFIXBASE="fde4:${GROUPNUMBER}"
PREFIXLEN=32
# You can reuse the above two to generate ip addresses/routes, ...
# e.g. "${PREFIXBASE}:1234::/$((PREFIXLEN+16))"

# This function describes the network topology that we want to emulate
function mk_topo {
    echo "@@ Adding links and nodes"
 
    #
    #                        ?
    #                        |
    #                        |
    #                        |
    #               P4------P1 ------ P3
    #                        \        /
    # Build a small network   \      /
    #                          \    /
    #                            P2
    #
    #       
    #
    # 
    #           
    #            AS4---P3---P4                  AS4: shared-cost
    #                 /       \             
    #        AS10--->P2       P5               AS10: We provide (back-up link)
    #               /           \
    #      AS7--->P1           P6              AS7: We provide
    #               \           /
    #       AS9 <---P0        P7               AS9: Our provider
    #                 \       /
    #                  P9---P8
    #
    #
    #


    # Nodes are creadted on the fly, and their interface are assigned as
    # <node name>-eth<count>, where count starts at 0 and is increased by 1
    # after each new interface

%for inter in data["interfaces"]:
%if ${inter["virtual"]}==False:
%if ${data["id"]}<${inter["id"]}:
#${data["name"]} links to ${inter["name"]}
add_link ${data["name"]} ${inter["name"]}
%endif
%endif
%if ${inter["virtual"]}==True:
bridge_node ${data["name"]} ${inter["bridge"]} ${inter["interface"]}
%endif
%endfor
}

