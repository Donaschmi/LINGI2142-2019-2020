all: clean create

old: 
	sudo ./create_network.sh my_topo_frrouting_conf

create:
	./auto_config_create.sh
	sudo ./create_network.sh my_auto_topo_conf


connect-P0:
	sudo ./connect_to.sh frrouting_cfg_auto/ P0

connect-P1:
	sudo ./connect_to.sh frrouting_cfg_auto/ P1

connect-P2:
	sudo ./connect_to.sh frrouting_cfg/ P2

connect-P3:
	sudo ./connect_to.sh frrouting_cfg/ P3

connect-P4:
	sudo ./connect_to.sh frrouting_cfg/ P4

clean:
	sudo ./cleanup.sh
