#/bin/bash

sysctl -w net.ipv6.conf.all.forwarding=1
sysctl -w net.ipv6.conf.default.forwarding=1

#BGP Policy: par defaut, on droppe tout pour les INPUT

ip6tables -P INPUT DROP

#FILTRES POUR ICMPV6
# On autorise l'entree de tous les messages d'information d'erreur ICMPV6
ip6tables -A INPUT -p icmpv6 --icmpv6-type destination-unreachable -j ACCEPT
ip6tables -A INPUT -p icmpv6 --icmpv6-type packet-too-big -j ACCEPT
ip6tables -A INPUT -p icmpv6 --icmpv6-type time-exceeded -j ACCEPT
ip6tables -A INPUT -p icmpv6 --icmpv6-type parameter-problem -j ACCEPT

# On autorise les pings, mais avec un ratio de 5 paquets max par minute
ip6tables -A INPUT -p icmpv6 --icmpv6-type echo-request -m limit --limit 5/min -j ACCEPT
ip6tables -A INPUT -p icmpv6 --icmpv6-type echo-reply -m limit --limit 5/min -j ACCEPT

# On autorise d'autres types ICMPv6 mais seulement ceux avec un Hop Limit de 255, ce qui assure
# que le message vient d'un de nos routeurs (sinon la valeur 255 aurait etee decrementee).
ip6tables -A INPUT -p icmpv6 --icmpv6-type router-advertisement -m hl --hl-eq 255 -j ACCEPT
ip6tables -A INPUT -p icmpv6 --icmpv6-type neighbor-solicitation -m hl --hl-eq 255 -j ACCEPT
ip6tables -A INPUT -p icmpv6 --icmpv6-type neighbor-advertisement -m hl --hl-eq 255 -j ACCEPT
ip6tables -A INPUT -p icmpv6 --icmpv6-type redirect -m hl --hl-eq 255 -j ACCEPT

# S'il n'y a pas eu de match, on applique la police par defaut, c'est a dire dropper tous les autres packets ICMPV6
ip6tables -A INPUT -p icmpv6 -j LOG --log-prefix "paquets ICMPv6 droppes"
ip6tables -A INPUT -p icmpv6 -j DROP

#FILTRES POUR UDP, TCP,esp
#On accepte les protocoles tcp, udp et esp avec un ratio de 5 paquets
#max par minute et venant seulement des adresses fe80::/16 et fde4::/16
ip6tables -A INPUT -p tcp -m limit --limit 5/min -s fe80::/16 -j ACCEPT
ip6tables -A INPUT -p udp -m limit --limit 5/min -s fe80::/16 -j ACCEPT
ip6tables -A INPUT -p esp -m limit --limit 5/min -s fe80::/16 -j ACCEPT
ip6tables -A INPUT -p tcp -m limit --limit 5/min -s fde4::/16 -j ACCEPT
ip6tables -A INPUT -p udp -m limit --limit 5/min -s fde4::/16 -j ACCEPT
ip6tables -A INPUT -p esp -m limit --limit 5/min -s fde4::/16 -j ACCEPT


#On accepte les paquets des autres protocoles comme OSPF, sans limite de paquets
#mais venant seulement aussi des adresses fe80::/16 et fde4::/16

ip6tables -A INPUT -s fe80::/16 -j ACCEPT
ip6tables -A INPUT -s fde4::/16 -j ACCEPT
ip6tables -A INPUT -j DROP
