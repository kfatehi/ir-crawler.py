LOGDIR=/home/kfatehi/public_html/crawler_logs
LOGSTAMP:=$(shell date +"%m-%d-%Y_%H-%M-%S")


cleandb:
	rm -f *.shelve

crawl: cleandb
	PYTHONUNBUFFERED=yes /usr/bin/python Crawler.py

crawl-log: 
	mkdir -p $(LOGDIR)/old
	-mv $(LOGDIR)/current.txt $(LOGDIR)/old/$(LOGSTAMP).txt
	cp js-logtail/* $(LOGDIR)
	touch $(LOGDIR)/current.txt
	chmod 755 $(LOGDIR)
	chmod 755 $(LOGDIR)/*
	wait
	make crawl > $(LOGDIR)/current.txt 2>&1 &
	tail -f $(LOGDIR)/current.txt
