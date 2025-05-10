CC = gcc
CFLAGS = -Wall -g -D_GNU_SOURCE
LDFLAGS = -lssl -lcrypto -lpam -lpthread
INC = -I.

all: client reverse_proxy

client: client.o tlsClient.o utils.o
	$(CC) -o client client.o tlsClient.o utils.o $(LDFLAGS)

reverse_proxy: reverseProxy.o tlsServer.o pamAuth.o httpClient.o utils.o tlsClient.o
	$(CC) -o reverse_proxy reverseProxy.o tlsServer.o pamAuth.o httpClient.o utils.o tlsClient.o $(LDFLAGS)

client.o: client.c tlsClient.h utils.h
	$(CC) $(CFLAGS) $(INC) -c client.c

tlsClient.o: tlsClient.c tlsClient.h utils.h
	$(CC) $(CFLAGS) $(INC) -c tlsClient.c

reverseProxy.o: reverseProxy.c tlsServer.h pamAuth.h httpClient.h utils.h
	$(CC) $(CFLAGS) $(INC) -c reverseProxy.c

tlsServer.o: tlsServer.c tlsServer.h utils.h
	$(CC) $(CFLAGS) $(INC) -c tlsServer.c

pamAuth.o: pamAuth.c pamAuth.h utils.h
	$(CC) $(CFLAGS) $(INC) -c pamAuth.c

httpClient.o: httpClient.c httpClient.h tlsClient.h utils.h
	$(CC) $(CFLAGS) $(INC) -c httpClient.c

utils.o: utils.c utils.h
	$(CC) $(CFLAGS) $(INC) -c utils.c

clean:
	rm -f *.o client reverse_proxy