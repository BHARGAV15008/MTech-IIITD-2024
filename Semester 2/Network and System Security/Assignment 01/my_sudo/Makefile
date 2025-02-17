CC = gcc
CFLAGS = -Wall -g
OBJ = main.o pathValidation.o privilegeManagement.o signalHandling.o

my_sudo: $(OBJ)
	$(CC) -o my_sudo $(OBJ)

%.o: %.c
	$(CC) $(CFLAGS) -c $<

clean:
	rm -f *.o my_sudo
