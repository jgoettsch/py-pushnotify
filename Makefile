clean:
	rm -rf dist build Manifest

test:
	nosetests --with-coverage --cover-package=pushnotify pushnotify/tests/tests.py

check:
	python setup.py check

build: test check
	python setup.py sdist bdist_wininst

upload: build
	python setup.py register sdist bdist_wininst upload
