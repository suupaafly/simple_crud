.PHONY: clean image publish_image

VERSION?=latest

IMAGE=zroom2/simple_crud


image: clean requirements
	@docker build --force-rm -t ${IMAGE}:${VERSION} -f Dockerfile .

publish_image: image
	@docker push ${IMAGE}:${VERSION}

clean:
	rm -rf dist build *.egg-info
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

requirements:
	pipenv lock -r > requirements.txt
