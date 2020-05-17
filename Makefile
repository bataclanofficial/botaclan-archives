PYTEST=pytest

all: test

test: unit-test

unit-test:
	$(PYTEST) --disable-warnings -vv -s .
