all: clean create

create: 
	sudo ./create_network.sh my_topo_frrouting_conf

auto-create:
	cd scripts/
	ls -l
	./script.py
	cd ..
	sudo rm -r frrouting_cfg_auto/*
	mv /script/tmp/* frrouting_cfg_auto/


connect-P1:
	sudo ./connect_to.sh frrouting_cfg/ P1

connect-P2:
	sudo ./connect_to.sh frrouting_cfg/ P2

connect-P3:
	sudo ./connect_to.sh frrouting_cfg/ P3

connect-P4:
	sudo ./connect_to.sh frrouting_cfg/ P4

clean:
	sudo ./cleanup.sh
