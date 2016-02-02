BUILD=_build
PGSQL=lib/postgresql-9.4.1207.jre6.jar
HIKARI=lib/HikariCP-2.4.3.jar
JDBC=jdbc.drivers=org.postgresql.Driver
CLASSPATH=.:$(ASSERT):$(JUNIT):$(PGSQL):$(HIKARI):$(BUILD)

SRC= \
		 src/*.java \
		 src/db/*.java

common-words: compile
	java -classpath $(CLASSPATH) -D$(JDBC) \
		-Dpg_password=$(shell cat _private/prod_db_password.txt) \
	 	ir.FindCommonWords

compile: clean
	@javac -g -d $(BUILD) -classpath $(CLASSPATH) $(SRC)

clean:
	@rm -rf $(BUILD)
	@mkdir -p $(BUILD)

crawl:
	node supervisor.js
