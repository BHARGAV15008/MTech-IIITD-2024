CC=gcc
CFLAGS=-Wall -Wextra -pedantic

parser.o: parser.c parser.h
	$(CC) $(CFLAGS) -c parser.c

execute.o: execute.c execute.h
	$(CC) $(CFLAGS) -c execute.c

redir.o: redir.c redir.h
	$(CC) $(CFLAGS) -c redir.c

prompt.o: prompt.c prompt.h
	$(CC) $(CFLAGS) -c prompt.c

shell.o: shell.c shell.h parser.h execute.h redir.h prompt.h
	$(CC) $(CFLAGS) -c shell.c

shell: parser.o execute.o redir.o prompt.o shell.o
	$(CC) $(CFLAGS) -o shell parser.o execute.o redir.o prompt.o shell.o

clean:
	rm -f *.o shell