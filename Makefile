LOGDIR=/home/kfatehi/public_html/crawler_logs
LOGSTAMP:=$(shell date +"%m-%d-%Y_%H-%M-%S")


cleandb:
	rm -f *.shelve

crawl:
	PYTHONUNBUFFERED=yes /usr/bin/python Crawler.py

crawl-log: make-logfile
	wait
	make crawl > $(LOGDIR)/current.txt 2>&1 &
	tail -f $(LOGDIR)/current.txt

resume:
	wait
	PYTHONUNBUFFERED=yes /usr/bin/python Crawler.py >> $(LOGDIR)/current.txt 2>&1 &
	tail -f $(LOGDIR)/current.txt

resume-supervised:
	node supervisor.js >> $(LOGDIR)/current.txt 2>&1

start-supervised: cleandb make-logfile
	echo "tail -f $(LOGDIR)/current.txt"
	node supervisor.js > $(LOGDIR)/current.txt 2>&1

make-logfile:
	mkdir -p $(LOGDIR)/old
	-mv $(LOGDIR)/current.txt $(LOGDIR)/old/$(LOGSTAMP).txt
	cp js-logtail/* $(LOGDIR)
	touch $(LOGDIR)/current.txt
	chmod 755 $(LOGDIR)
	chmod 755 $(LOGDIR)/*

test-whitelist:
	@cat /home/kfatehi/public_html/crawler_logs/old/all-rejects.txt | grep Reject | /usr/bin/python UrlValidator.py
