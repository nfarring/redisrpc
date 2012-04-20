BASIC_TARGETS:=\
	README.html

RUBY_TARGETS:=

PHP_TARGETS:=\
	composer.phar\
	php/vendor

PYTHON_TARGETS:=\
	python/LICENSE\
	python/README.rst\
	python/dist

.PHONY: help
help:
	@echo 'Build Targets:'
	@echo '  all'
	@echo '  ruby'
	@echo '  php'
	@echo '  python'
	@echo 'Clean Targets:'
	@echo '  clean-all'
	@echo '  clean-ruby'
	@echo '  clean-php'
	@echo '  clean-python'

.PHONY: all
all: basic ruby php python

.PHONY: basic
basic: $(BASIC_TARGETS)

.PHONY: ruby
ruby: basic $(RUBY_TARGETS)

.PHONY: php
php: basic $(PHP_TARGETS)

.PHONY: python
python: basic $(PYTHON_TARGETS)

.PHONY: clean-all
clean-all: clean-basic clean-ruby clean-php clean-python

.PHONY: clean-basic
clean-basic:
	@rm -rf $(BASIC_TARGETS)

.PHONY: clean-ruby
clean-ruby:
	@rm -rf $(RUBY_TARGETS)
	@rm -rf ruby/*.gem

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

########################
# Rules for Ruby Targets
########################

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
