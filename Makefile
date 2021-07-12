<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
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
=======
CC=g++ 
CFLAGS= -std=gnu++11 -O2
DEBUG=-g
SRC=src
EXEC=build
OBJ=build

all: $(EXEC)/main

$(EXEC)/main: $(OBJ)/conv2d_layer.o $(OBJ)/filter.o $(SRC)/main.cpp
	$(CC) $(CFLAGS) $(SRC)/main.cpp -o  $(EXEC)/main

$(OBJ)/conv2d_layer.o: $(SRC)/conv2d_layer.hpp $(OBJ)/filter.o
	$(CC) $(CFLAGS) $(SRC)/conv2d_layer.hpp -o $(OBJ)/conv2d_layer.o

$(OBJ)/filter.o: $(SRC)/filter.hpp
	$(CC) $(CFLAGS) $(SRC)/filter.hpp -o $(OBJ)/filter.o

clean: 
	rm $(OBJ)/*.o $(EXEC)/main
>>>>>>> cd21a41 (디렉토리 구조 및 README 수정)
=======
CC=g++ 
CFLAGS= -std=gnu++11 -O2
DEBUG=-g
SRC=src
EXEC=c_executions
OBJ=c_object_files

all: $(EXEC)/main

$(EXEC)/main: $(OBJ)/conv2d_layer.o $(OBJ)/filter.o $(SRC)/main.cpp
	$(CC) $(CFLAGS) $(SRC)/main.cpp -o  $(EXEC)/main

$(OBJ)/conv2d_layer.o: $(SRC)/conv2d_layer.hpp $(OBJ)/filter.o
	$(CC) $(CFLAGS) $(SRC)/conv2d_layer.hpp -o $(OBJ)/conv2d_layer.o

$(OBJ)/filter.o: $(SRC)/filter.hpp
	$(CC) $(CFLAGS) $(SRC)/filter.hpp -o $(OBJ)/filter.o

clean: 
	rm $(OBJ)/*.o $(EXEC)/main
>>>>>>> 626fa86 (디렉토리명 변경에 따른 수정)
=======
CC=g++ 
CFLAGS= -std=c++17
DEBUG=-g
SRC=src
EXEC=c_executions
OBJ=c_object_files

all: $(EXEC)/main

$(EXEC)/main: $(OBJ)/conv2d_layer.o $(OBJ)/filter.o $(SRC)/main.cpp
	$(CC) $(CFLAGS) $(SRC)/main.cpp -o  $(EXEC)/main -lstdc++fs

$(OBJ)/conv2d_layer.o: $(SRC)/conv2d_layer.hpp $(OBJ)/filter.o
	$(CC) -c $(CFLAGS) $(SRC)/conv2d_layer.hpp -o $(OBJ)/conv2d_layer.o

$(OBJ)/filter.o: $(SRC)/filter.hpp
	$(CC) -c $(CFLAGS) $(SRC)/filter.hpp -o $(OBJ)/filter.o

clean: 
	rm $(OBJ)/*.o $(EXEC)/main
>>>>>>> e3d6fb7 (적절한 컴파일러 옵션 추가)
