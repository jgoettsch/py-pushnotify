clean:
	rm -rf dist/* build/* Manifest

test:
	python setup.py nosetests

check:
	python setup.py check

build: check
	python setup.py sdist --formats=gztar,zip bdist_wininst

upload: build
	python setup.py register sdist --formats=gztar,zip bdist_wininst upload
