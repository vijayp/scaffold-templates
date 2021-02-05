# Simple makefile that has a bunch of stuff that we care about.

# 1. you can run all tests with "make test"
test:
	cd py && /usr/bin/env python3 -m unittest discover -p '*unittest.py' -v ; cd -


# 2. you can create a docker file with make docker
docker: .phony

all: test