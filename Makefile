PACKAGE := releasecmd
PYTHON := python3


.PHONY: build
build: clean
	$(PYTHON) -m tox -e build
	ls -lh dist/*

.PHONY: check
check:
	$(PYTHON) -m tox -e lint

.PHONY: clean
clean:
	$(PYTHON) -m tox -e clean

.PHONY: fmt
fmt:
	$(PYTHON) -m tox -e fmt

.PHONY: release
release:
	$(PYTHON) setup.py release --sign --skip-uploading --verbose
	$(MAKE) clean

.PHONY: setup-ci
setup-ci:
	$(PYTHON) -m pip install -q --disable-pip-version-check --upgrade pip
	$(PYTHON) -m pip install -q --disable-pip-version-check --upgrade tox

.PHONY: setup
setup: setup-ci
	$(PYTHON) -m pip install -q --disable-pip-version-check --upgrade -e . setuptools
	$(PYTHON) -m pip check

.PHONY: test
test:
	$(PYTHON) setup.py release --skip-tagging --verbose --use-installed-version --dry-run
