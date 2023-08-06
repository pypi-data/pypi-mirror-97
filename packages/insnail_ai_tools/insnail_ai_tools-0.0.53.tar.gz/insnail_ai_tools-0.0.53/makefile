test:
	pytest

clean:
	rm -rf build dist insnail_ai_tools.egg-info .pytest*

build:
	python setup.py sdist bdist_wheel

publish:
	twine upload --repository pypi dist/*

release:
	make test
	make clean
	make build
	make publish