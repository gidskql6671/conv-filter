CC=g++ 
CFLAGS= -std=gnu++11 -O2
DEBUG=-g
SRC=src
EXEC=src/executions
OBJ=src/objects

all: main

main: conv2d_layer.o filter.o main.cpp
	$(CC) $(CFLAGS) $(SRC)/main.cpp -o  $(EXEC)/main

conv2d_layer.o: conv2d_layer.hpp filter.o
	$(CC) $(CFLAGS) $(SRC)/conv2d_layer.hpp -o $(OBJ)/conv2d_layer.o

filter.o: filter.hpp
	$(CC) $(CFLAGS) $(SRC)/filter.hpp -o $(OBJ)/filter.o

clean: 
	rm $(OBJ)/*.o $(EXEC)/main
