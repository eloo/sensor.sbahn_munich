
include .env
export $(shell sed 's/=.*//' .env)

.PHONY: dependencies
dependencies:
	pip3 install -r requirements_test.txt

.PHONY: test
test:
	pytest tests