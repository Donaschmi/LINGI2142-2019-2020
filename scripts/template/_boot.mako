#/bin/bash

sysctl -w net.ipv6.conf.all.forwarding=1
sysctl -w net.ipv6.conf.default.forwarding=1

#ip6tables -N EXTERNAL
#ip6tables -A EXTERNAL -j DROP

#ip6tables -A INPUT -s fde4:8:0::7/128 -j EXTERNAL 
#ip6tables -A OUTPUT -s fde4:8:0::7/128 -j EXTERNAL
#ip6tables -A FORWARD -s fde4:8:0::7/128 -j EXTERNAL 


#ip6tables -N DDOS
#ip6tables -A DDOS -p icmpv6 -m limit --limit 2/min -j DROP
#ip6tables -A DDOS -p icmpv6 -j DROP
#ip6tables -A DDOS -p icmpv6 --icmpv6-type echo-request -m limit --limit 5/min -j ACCEPT
#ip6tables -A DDOS -p icmpv6 --icmpv6-type echo-reply -m limit --limit 5/min -j ACCEPT
#ip6tables -A DDOS -m limit --limit 0/min -j DROP
#-j LOG --log-prefix "ip6tables - drop (private addr):       " --log-level 4
#ip6tables -A DDOS -j DROP

#ip6tables -A INPUT -s fde4:8:0::6/128 -j DDOS
#ip6tables -A OUTPUT -s fde4:8:0::6/128 -j DDOS
#ip6tables -A FORWARD -s fde4:8:0::6/128 -j DDOS

#ip6tables -A INPUT -s fde4:8:00:36::6/64 -j DDOS
#ip6tables -A OUTPUT -s fde4:8:00:36::6/64 -j DDOS
#ip6tables -A FORWARD -s fde4:8:00:36::6/64 -j DDOS

#ip6tables -A INPUT -s fde4:8:00:56::6/64 -j DDOS
#ip6tables -A OUTPUT -s fde4:8:00:56::6/64 -j DDOS
#ip6tables -A FORWARD -s fde4:8:00:56::6/64 -j DDOS

# Flush chains

ip6tables -F INPUT
ip6tables -F FORWARD
ip6tables -F OUTPUT
ip6tables -F

# Set up default policies

ip6tables -P INPUT -p icmpv6 DROP
ip6tables -P FORWARD -p icmpv6 DROP
ip6tables -P OUTPUT -p icmpv6 DROP


# Allow some ICMPv6 types in the INPUT chain
# Using ICMPv6 type names to be clear.

ip6tables -A INPUT -p icmpv6 --icmpv6-type destination-unreachable -j ACCEPT
ip6tables -A INPUT -p icmpv6 --icmpv6-type packet-too-big -j ACCEPT
ip6tables -A INPUT -p icmpv6 --icmpv6-type time-exceeded -j ACCEPT
ip6tables -A INPUT -p icmpv6 --icmpv6-type parameter-problem -j ACCEPT


# Allow some other types in the INPUT chain, but rate limit.
ip6tables -A INPUT -p icmpv6 --icmpv6-type echo-request -m limit --limit 5/min -j ACCEPT
ip6tables -A INPUT -p icmpv6 --icmpv6-type echo-reply -m limit --limit 5/min -j ACCEPT


# Allow others ICMPv6 types but only if the hop limit field is 255.

ip6tables -A INPUT -p icmpv6 --icmpv6-type router-advertisement -m hl --hl-eq 255 -j ACCEPT
ip6tables -A INPUT -p icmpv6 --icmpv6-type neighbor-solicitation -m hl --hl-eq 255 -j ACCEPT
ip6tables -A INPUT -p icmpv6 --icmpv6-type neighbor-advertisement -m hl --hl-eq 255 -j ACCEPT
ip6tables -A INPUT -p icmpv6 --icmpv6-type redirect -m hl --hl-eq 255 -j ACCEPT


# When there isn't a match, the default policy (DROP) will be applied.
# To be sure, drop all other ICMPv6 types.
# We're dropping enough icmpv6 types to break RFC compliance.

ip6tables -A INPUT -p icmpv6 -j LOG --log-prefix "dropped ICMPv6"
ip6tables -A INPUT -p icmpv6 -j DROP


# Allow ICMPv6 types that should be sent through the Internet.

ip6tables -A OUTPUT -p icmpv6 --icmpv6-type destination-unreachable -j ACCEPT
ip6tables -A OUTPUT -p icmpv6 --icmpv6-type packet-too-big -j ACCEPT
ip6tables -A OUTPUT -p icmpv6 --icmpv6-type time-exceeded -j ACCEPT
ip6tables -A OUTPUT -p icmpv6 --icmpv6-type parameter-problem -j ACCEPT
