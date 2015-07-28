GAE_ZIP = google_appengine_1.9.24.zip
GAE_URL = https://storage.googleapis.com/appengine-sdks/featured/$(GAE_ZIP)
GAE_SERVER = tmp/google_appengine/dev_appserver.py

clean:
	rm -rf lib/ venv/

venv:
	virtualenv venv

git-hooks:
	cp git_hooks/* .git/hooks/

install: clean git-hooks venv
	pip install -r requirements.txt -t lib/ --ignore-installed; \
	. venv/bin/activate; \
	pip install flake8; \
	pip install nose; pip install nosegae;\

create-tmp:
	mkdir -p tmp

gae-install: create-tmp
	curl $(GAE_URL) -o tmp/$(GAE_ZIP) -z tmp/$(GAE_ZIP); \
	unzip -o tmp/$(GAE_ZIP) -d tmp/

venv-install: create-tmp
	sudo pip install virtualenv

tool-install: gae-install venv-install

server:
	python $(GAE_SERVER) .

test:
	. venv/bin/activate; \
	nosetests tests --with-gae --gae-lib-root=tmp/google_appengine

flake8:
	. venv/bin/activate; flake8 app tests --max-line-length=100
