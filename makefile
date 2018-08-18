PYTHON	:= python3.6
PIP	:= PIP10.0



ScieBeam:
	git clone https://github.com/SuperYuLu/scibeam

##
# To be implemented
##

#FILES :=
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

config:
	git config -l

status:
	make clean
	@echo
	git branch
	git remote -v
	git status

test:
	python setup.py test


doc:
	pandoc --from=markdown  --to=rst --output=README.rst README.md

coverage:
	coverage rum setup.py test
	coverage report -m 
build:
	python setup.py sdist bdist_wheel

rbuild:
	rm -r build dist

test-pypi:
	twine upload --repository-url https://test.pypi.org/legacy/ ./dist/*


