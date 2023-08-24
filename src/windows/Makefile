GCOV=-fprofile-arcs -ftest-coverage
all: install

UNAME:=$(shell uname -s)
ifeq ($(UNAME),Linux)
	LIBS=-lcheck -lsubunit -lrt -lm -lpthread
	LEAKS_IN = valgrind --leak-check=full
endif 
ifeq ($(UNAME),Darwin)
	LIBS=-lcheck -lm
	LEAKS_IN = leaks -atExit --
endif

install:
	pip install -r requirements.txt
	gcc -shared -o main.dll main.c
	../sane_mkdir.exe ../calculator 
	../sane_mkdir.exe ../calculator/build
	../sane_mkdir.exe ../calculator/build/install_windows
	../sane_cp.exe install_windows/cat-monday-left-me-broken-cat.gif install_windows/cat-small.gif ../calculator/build/install_windows/
	../sane_cp.exe errors.py main.py main.dll ../calculator/build/
	../sane_cp.exe install_windows/calculator.bat ../calculator/
	make clean

uninstall:
	../sane_rm.exe ../calculator 

build:
	gcc -shared -o main.dll main.c
	python main.py
	
test:
	gcc -g test.c $(LIBS) -o test 
	./test

gcov_report:
	gcc $(CFLAGS) $(GCOV) test.c $(LIBS)  -o GcovReport
	./GcovReport
	lcov -t "GcovReport" -o GcovReport.info -c -d .
	genhtml -o report GcovReport.info 

clean:
	../sane_rm.exe ./*.o ./*.a ./a.out ./GcovReport ./*.gcno ./*.gcda ./report ./*.info *.dll 
	../sane_rm.exe *.exe *.ddl expression.c expression c_execute test __pycache__

dist: clean
	cd .. && tar -czvf s21_calc.tar.gz *

dvi:
	echo %OS% | findstr /i "Windows" >nul && (start ../dvi.md) || (xdvi dvi.md)

clang_format:
	cp ../materials/linters/.clang-format .
	clang-format -n *.c 

clang_formating:
	clang-format --style=google -i *.c 
