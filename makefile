#FILES :=                              

# ifeq ($(shell uname), Darwin)          # Apple
#     PYTHON   := python3.6
#     PIP      := pip10.0
#     PYLINT   := pylint
#     COVERAGE := coverage-3.5
#     PYDOC    := pydoc3.5
#     AUTOPEP8 := autopep8
# else ifeq ($(CI), true)                # Travis CI
#     PYTHON   := python3.6
#     PIP      := pip10.0
#     PYLINT   := pylint
#     COVERAGE := coverage-3.5
#     PYDOC    := pydoc3
#     AUTOPEP8 := autopep8
# else ifeq ($(shell uname -p), unknown) # Docker
#     PYTHON   := python                # on my machine it's python
#     PIP      := pip10.0
#     PYLINT   := pylint
#     COVERAGE := coverage-3.5
#     PYDOC    := python -m pydoc        # on my machine it's pydoc 
#     AUTOPEP8 := autopep8
# else                                   # UTCS
#     PYTHON   := python3.6
#     PIP      := pip10
#     PYLINT   := pylint3
#     COVERAGE := coverage-3.5
#     PYDOC    := pydoc3.5
#     AUTOPEP8 := autopep8
# endif

PYTHON	:= python3.6
PIP	:= PIP10.0



ScieBeam:
	git clone https://github.com/SuperYuLu/scibeam

# check:
# 	@not_found=0;                                 \
#     for i in $(FILES);                            \
#     do                                            \
#         if [ -e $$i ];                            \
#         then                                      \
#             echo "$$i found";                     \
#         else                                      \
#             echo "$$i NOT FOUND";                 \
#             not_found=`expr "$$not_found" + "1"`; \
#         fi                                        \
#     done;                                         \
#     if [ $$not_found -ne 0 ];                     \
#     then                                          \
#         echo "$$not_found failures";              \
#         exit 1;                                   \
#     fi;                                           \
#     echo "success";

clean:
	rm *~
#	rm -rf __pycache__

config:
	git config -l

status:
	make clean
	@echo
	git branch
	git remote -v
	git status

test:	
	python unittests/test_base.py
	python unittests/test_core_common.py
	python unittests/test_core_tof.py
