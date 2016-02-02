BUILD=_build
PGSQL=lib/postgresql-9.4.1207.jre6.jar
JDBC=jdbc.drivers=org.postgresql.Driver
CLASSPATH=.:$(PGSQL):$(BUILD):$(SLF4J)

SRC= \
		 src/*.java \
		 src/db/*.java

common-words: compile
	echo "this will take awhile, please wait!!!"
	java -classpath $(CLASSPATH) -D$(JDBC) \
	 	ir.analysis.FindCommonWords > words.txt

subdomains: compile
	java -classpath $(CLASSPATH) -D$(JDBC) \
	 	ir.analysis.FindSubDomains

compile: clean
	@javac -g -d $(BUILD) -classpath $(CLASSPATH) $(SRC)

clean:
	@rm -rf $(BUILD)
	@mkdir -p $(BUILD)

crawl:
	node supervisor.js
