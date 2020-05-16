PYTEST=pytest

all: test

test:
		$(PYTEST) --disable-warnings -vv -s .
unit-test:
	$(PYTEST) --disable-warnings -vv -s .
