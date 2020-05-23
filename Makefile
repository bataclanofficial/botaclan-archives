PYTEST=pytest

all: test

test: unit-test

unit-test:
	BOTACLAN_DISABLE_CLI="" $(PYTEST) --disable-warnings -vv -s .

remove-cache:
	find . | grep -E "(__pycache__|\.pyc|\.pyo$|\.pytest_cache)" | xargs rm -rf
