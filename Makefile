lint:
	black --check holmium tests
	ruff holmium tests

lint-fix:
	black holmium tests
	isort -r --profile=black holmium tests
	ruff --fix holmium tests
