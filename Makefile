app_name=color-palette
app_port=80

setup:
	# Only run on development machines
	python3 -m venv /tmp/venv
	. /tmp/venv/bin/activate

install:
	# Run once python venv is activated on development machines
	pip3 install --upgrade pip &&\
	pip3 install -r requirements.txt

lint-app:
	# Pull hadolint Docker image if running on CI
ifeq ($(CI), true)
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
	docker run -d -p 8000:$(app_port) $(app_name)

test-app:
	$(MAKE) run-app
	pwd
	cd test && pytest

all: setup install lint-app lint-infra