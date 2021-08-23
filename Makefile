install-linux-base:
	mkdir -p /usr/local/sbin
	cp linux-base/* /usr/local/sbin
	chmod +x /usr/local/sbin/*
	chmod ug+r /usr/local/sbin/*

add-ec2-sumo-source:
	@chmod +x *
	./sumologic/add-ec2-sumo-source.py

add-eb-sumo-source:
	@chmod +x *
	./sumologic/add-eb-sumo-source.py
