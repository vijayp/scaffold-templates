# Simple makefile that has a bunch of stuff that we care about.
venv-setup:
	/usr/bin/env python3 -m venv venv && . venv/bin/activate && pip install --upgrade pip && pwd && pip install -r py/requirements.txt

venv-freeze:
	. venv/bin/activate && pip freeze > py/requirements.txt

venv-clean:
	rm -rf venv

# 1. you can run all tests with "make test"
test:
	cd py && /usr/bin/env python3 -m unittest discover -p '*unittest.py' -v ; cd -


# 2. you can create a docker file with make docker
docker:
	docker build .

setup: venv-setup
all: test