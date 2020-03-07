PACKAGE := releasecmd


.PHONY: build
build:
	@make clean
	@tox -e build
	ls -lh dist/*

.PHONY: check
check:
	@tox -e lint

.PHONY: clean
clean:
	@tox -e clean

.PHONY: fmt
fmt:
	@tox -e fmt

.PHONY: release
release:
	@tox -e release
	@make clean

.PHONY: release
release:
	@python setup.py release --sign

.PHONY: setup
setup:
	@pip install --upgrade -e . tox
