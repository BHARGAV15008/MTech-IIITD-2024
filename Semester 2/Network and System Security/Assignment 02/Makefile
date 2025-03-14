CC = gcc
CFLAGS = -Wall -Wextra -I./include
LDFLAGS = -lssl -lcrypto -pthread

$(shell mkdir -p bin)

all: bin/kdcServer bin/prnSrv bin/client

bin/kdcServer: src/kdcServer.c src/cryptoUtils.c src/logger.c
	$(CC) $^ -o $@ $(CFLAGS) $(LDFLAGS)

bin/prnSrv: src/prnSrv.c src/cryptoUtils.c src/logger.c
	$(CC) $^ -o $@ $(CFLAGS) $(LDFLAGS)

bin/client: src/client.c src/cryptoUtils.c src/logger.c
	$(CC) $^ -o $@ $(CFLAGS) $(LDFLAGS)

clean:
	rm -f bin/* *.log