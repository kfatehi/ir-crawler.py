LOGDIR=/home/kfatehi/public_html/crawler_logs
LOGSTAMP:=$(shell date +"%m-%d-%Y_%H-%M-%S")

crawl:
	PYTHONUNBUFFERED=yes /usr/bin/python Crawler.py

resume-supervised:
	node supervisor.js

start-supervised: rotate-logfile
	node supervisor.js

rotate-logfile:
	mkdir -p $(LOGDIR)/old
	-mv $(LOGDIR)/current.txt $(LOGDIR)/old/$(LOGSTAMP).txt
	cp js-logtail/* $(LOGDIR)
	touch $(LOGDIR)/current.txt
	chmod 755 $(LOGDIR)
	chmod 755 $(LOGDIR)/*
