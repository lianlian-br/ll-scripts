install-linux-base:
	mkdir -p /usr/local/sbin
	cp linux-base/* /usr/local/sbin
	chmod +x /usr/local/sbin/*
	chmod ug+r /usr/local/sbin/*

add-ec2-sumo-source:
	@chmod +x *
	./sumologic/add_ec2_sumo_source.py

add-eb-sumo-source:
	@chmod +x *
	./sumologic/add_eb_sumo_source.py

start-collector:
	service collector restart