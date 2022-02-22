.PHONY: test

include .env
export $(shell sed 's/=.*//' .env)

test:
	pytest tests