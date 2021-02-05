# Simple makefile that has a bunch of stuff that we care about.
venv-setup:
	cd py && python3 -m venv venv && . venv/bin/activate && pip install --upgrade pip && pwd && pip install -r requirements.txt

venv-freeze:
	cd py && . venv/bin/activate && pip freeze > requirements.txt

venv-clean:
	cd py && rm -rf venv

# 1. you can run all tests with "make test"
test:
	cd py && /usr/bin/env python3 -m unittest discover -p '*unittest.py' -v ; cd -


# 2. you can create a docker file with make docker
docker:
	docker build .

setup: venv-setup
all: test