all: build
build:
	gcc -shared -o main.dll main.c
	python main.py
clean:
	rm -rf ./*.o ./*.a ./a.out ./GcovReport ./*.gcno ./*.gcda ./report ./*.info *.dll 
	rm -rf *.exe *.ddl expression.c expression c_execute 
