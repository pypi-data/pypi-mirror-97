clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

dist: clean-build ## builds source and wheel package
	python setup.py sdist bdist_wheel

release: dist ## package and upload a release
	python -m twine upload dist/*

