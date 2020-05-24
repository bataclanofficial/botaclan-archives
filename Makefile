PYTEST=pytest
PRE-COMMIT=pre-commit

all: test

test: unit-test

unit-test:
	BOTACLAN_DISABLE_CLI="" $(PYTEST) --disable-warnings -vv -s .

pre-commit:
	$(PRE-COMMIT) run --all-files -v

remove-cache:
	find . | grep -E "(__pycache__|\.pyc|\.pyo$|\.pytest_cache)" | xargs rm -rf
