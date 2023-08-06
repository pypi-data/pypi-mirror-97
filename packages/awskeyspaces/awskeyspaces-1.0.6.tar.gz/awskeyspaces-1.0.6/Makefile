SHELL=/bin/bash

download-key:
	curl https://www.amazontrust.com/repository/AmazonRootCA1.pem -O

dev:
	pip3.8 install --user -r requirements-dev.txt

prod:
	pip3.8 install -r requirements.txt

init: download-key dev
	
