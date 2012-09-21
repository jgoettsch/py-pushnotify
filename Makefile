clean:
	rm -rf dist/* build/* Manifest

test:
	nosetests --with-coverage --cover-package=pushnotify pushnotify/tests/tests.py

.PHONY: docs
docs:
	epydoc --name pushnotify --url https://bitbucket.org/jgoettsch/py-pushnotify/ --docformat plaintext --exclude .*keys --exclude abstract --html pushnotify -o docs
	hg add docs

upload_docs: docs
	python setup.py upload_docs --upload-dir=docs

check:
	python setup.py check

build: check
	python setup.py sdist --formats=gztar,zip bdist_wininst

upload: build
	python setup.py register sdist --formats=gztar,zip bdist_wininst upload
