BASIC_TARGETS:=\
	README.html

PHP_TARGETS:=\
	$(BASIC_TARGETS)\
	composer.phar\
	php/vendor

PYTHON_TARGETS:=\
	$(BASIC_TARGETS)\
	python/LICENSE\
	python/README.rst\
	python/dist

ALL_TARGETS:=\
	$(BASIC_TARGETS)\
	$(PHP_TARGETS)\
	$(PYTHON_TARGETS)

.PHONY: help
help:
	@echo 'Build Targets:'
	@echo '  all'
	@echo '  php'
	@echo '  python'
	@echo 'Clean Targets:'
	@echo '  clean-all'
	@echo '  clean-php'
	@echo '  clean-python'

.PHONY: all
all: $(ALL_TARGETS)

.PHONY: basic
basic: $(BASIC_TARGETS)

.PHONY: php
php: $(PHP_TARGETS)

.PHONY: python
python: $(PYTHON_TARGETS)

.PHONY: clean-all
clean-all: clean-php clean-python

.PHONY: clean-php
clean-php:
	@rm -rf $(PHP_TARGETS)
	@rm -rf composer.lock

.PHONY: clean-python
clean-python:
	@rm -rf $(PYTHON_TARGETS)
	@rm -rf python/*.pyc python/examples/*.pyc
	@rm -rf python/build
	@rm -rf python/redisrpc.egg-info

#########################
# Rules for Basic Targets
#########################

# Ref: https://github.com/alampros/Docter
README.html: README.markdown
	docs/github-flavored-markdown.rb $< >$@

#######################
# Rules for PHP Targets
#######################

composer.phar:
	curl -s http://getcomposer.org/installer | php

php/vendor: composer.phar
	php composer.phar install

##########################
# Rules for Python Targets
##########################

python/LICENSE: LICENSE
	cp -a $< $@

python/README.rst: README.html
	cat $< | pandoc --from=html --to=rst --output=$@

python/dist: python/LICENSE python/README.rst
	cd python && python setup.py sdist
