all: clean create

old: 
	sudo ./create_network.sh my_topo_frrouting_conf

create:
	./auto_config_create.sh
	sudo ./create_network.sh my_auto_topo_conf

last:
	sudo ./create_network.sh my_auto_topo_conf

connect-P0:
	sudo ./connect_to.sh frrouting_cfg/ P0

connect-P1:
	sudo ./connect_to.sh frrouting_cfg/ P1

connect-P2:
	sudo ./connect_to.sh frrouting_cfg/ P2

connect-P3:
	sudo ./connect_to.sh frrouting_cfg/ P3

connect-P4:
	sudo ./connect_to.sh frrouting_cfg/ P4

connect-P5:
	sudo ./connect_to.sh frrouting_cfg/ P5

connect-P6:
	sudo ./connect_to.sh frrouting_cfg/ P6

connect-P7:
	sudo ./connect_to.sh frrouting_cfg/ P7

connect-P8:
	sudo ./connect_to.sh frrouting_cfg/ P8

connect-P9:
	sudo ./connect_to.sh frrouting_cfg/ P9
clean:
	sudo ./cleanup.sh
