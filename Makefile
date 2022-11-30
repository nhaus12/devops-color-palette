app_name=color-palette
app_port=80

setup:
	python3 -m venv /tmp/venv
	source /tmp/venv/bin/activate

install:
	# Run once python venv is activated
	pip install --upgrade pip &&\
	pip install -r requirements.txt

lint-app:
	# Conditional execution based on whether running on CI
ifeq ($(CI), 1)
	docker pull hadolint/hadolint
	docker run --rm -i hadolint/hadolint < Dockerfile
else
	hadolint Dockerfile
endif
	pylint --disable=R,C,W1203,W1202,W0703 app.py

lint-infra:
	# TODO
	echo "TODO"

build-app:
	docker build . --tag=$(app_name)

run-app:
	docker run -p 8000:$(app_port) $(app_name)

all: setup install lint-app lint-infra