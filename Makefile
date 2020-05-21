PYTEST=pytest

all: test

test: unit-test

unit-test:
	BOTACLAN_DISABLE_CLI="" $(PYTEST) --disable-warnings -vv -s .
