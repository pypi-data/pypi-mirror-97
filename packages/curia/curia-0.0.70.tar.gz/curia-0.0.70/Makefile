.PHONY: clean install test lint build-api

#################################################################################
# GLOBALS                                                                       #
#################################################################################

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Delete all compiled Python files
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

install:
	python setup.py install

test: install
	python setup.py pytest

lint:
	pylint -r n src test

build-api: install
	java -jar swagger-codegen-cli.jar generate -i https://api.curia.ai/-json -l python -o src/curia/api
	find src/curia/api -type f -exec sed -i 's/^from swagger_client/from curia.api.swagger_client/g' {} +
	find src/curia/api -type f -exec sed -i 's/^import swagger_client/import curia.api.swagger_client/g' {} +
	find src/curia/api -type f -exec sed -i 's/swagger_client.models, klass/curia.api.swagger_client.models, klass/g' {} +
	touch src/curia/api/__init__.py

build-api-dev : install
	java -jar swagger-codegen-cli.jar generate -i https://api.dev.curia.ai/-json -l python -o src/curia/api
	find src/curia/api -type f -exec sed -i 's/^from swagger_client/from curia.api.swagger_client/g' {} +
	find src/curia/api -type f -exec sed -i 's/^import swagger_client/import curia.api.swagger_client/g' {} +
	find src/curia/api -type f -exec sed -i 's/swagger_client.models, klass/curia.api.swagger_client.models, klass/g' {} +
	touch src/curia/api/__init__.py