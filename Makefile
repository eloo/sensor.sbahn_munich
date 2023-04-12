
include .env
export $(shell sed 's/=.*//' .env)

.PHONY: dependencies
dependencies:
	pip3 install -r requirements_test.txt

.PHONY: test
test:
	pytest tests

update-blueprint:
	wget -N https://raw.githubusercontent.com/ludeeus/integration_blueprint/main/scripts/develop -P scripts
	wget -N https://raw.githubusercontent.com/ludeeus/integration_blueprint/main/scripts/lint -P scripts
	wget -N https://raw.githubusercontent.com/ludeeus/integration_blueprint/main/scripts/setup -P scripts
	chmod -R +x scripts
	wget -N https://raw.githubusercontent.com/ludeeus/integration_blueprint/main/requirements.txt
	wget -N https://raw.githubusercontent.com/ludeeus/integration_blueprint/main/.devcontainer.json
