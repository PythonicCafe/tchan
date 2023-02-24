lint:
	autoflake --in-place --recursive --remove-unused-variables --remove-all-unused-imports .
	isort --skip migrations --skip wsgi --skip asgi --line-length 80 --multi-line VERTICAL_HANGING_INDENT --trailing-comma .
	black --exclude '(docker/|migrations/|config/settings\.py|manage\.py|\.direnv|\.eggs|\.git|\.hg|\.mypy_cache|\.nox|\.tox|\.venv|venv|\.svn|\.ipynb_checkpoints|_build|buck-out|build|dist|__pypackages__)' -l 80 .
	flake8 --config setup.cfg

test:
	pytest

test-v:
	pytest -vvv

test-release:
	rm -rf build dist
	python setup.py sdist bdist_wheel
	twine check dist/*
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

release:
	rm -rf build dist
	python setup.py sdist bdist_wheel
	twine check dist/*
	twine upload dist/*

.PHONY: lint test test-v test-release release
