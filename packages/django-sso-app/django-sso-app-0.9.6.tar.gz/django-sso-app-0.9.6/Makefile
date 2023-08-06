DOCKER=docker
DPATH=${CURDIR}
IMAGE_NAME=django-sso-app
#VERSION=$(shell python setup.py --version | sed 's/\.post.*//' | sed 's/\+g.*//')
VERSION=0.9.6

export DPATH
.PHONY:	clean build publish build-docker push-docker

clean:
	rm -rf ./dist/*
	rm -rf ./build/*
	rm -rf  ./src/django_sso_app.egg-info
	find ./src -name *.pyc -exec rm {} \;

build-release: clean
	python setup.py sdist bdist_wheel

publish:
	twine upload dist/* --verbose

build-docker: clean
	$(DOCKER) build . --network host -f ./compose/production/django/Dockerfile -t paiuolo/${IMAGE_NAME} -t paiuolo/${IMAGE_NAME}:${VERSION}

push-docker:
	$(DOCKER) push paiuolo/${IMAGE_NAME}:${VERSION}
	$(DOCKER) push paiuolo/${IMAGE_NAME}:latest
