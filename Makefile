VERSION:=$(shell cat VERSION)

BASIC_TARGETS:=\
	README.html

RUBY_TARGETS:=\
    ruby/lib/redisrpc/version.rb

PHP_TARGETS:=\
	composer.phar\
	php/vendor

PYTHON_TARGETS:=\
	python/VERSION\
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
	@echo 'Test Targets:'
	@echo '  test-python'

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
	@rm -rf python/*.egg
	@rm -rf python/*.log
	@rm -rf python/build
	@rm -rf python/redisrpc.egg-info
	@rm -rf python/.tox

.PHONY: test-python
test-python: python
	cd python && tox

#########################
# Rules for Basic Targets
#########################

# Ref: https://github.com/alampros/Docter
README.html: README.markdown
	docs/github-flavored-markdown.rb $< >$@

########################
# Rules for Ruby Targets
########################

ruby/lib/redisrpc:
	mkdir $@

ruby/lib/redisrpc/version.rb: ruby/lib/redisrpc
	printf "module RedisRPC\n" >$@
	printf "  #Ref: http://semver.org/\n" >>$@
	printf "  VERSION = '%s'\n" $(VERSION) >>$@
	printf "end\n" >>$@

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

python/VERSION: VERSION
	cp -a $< $@

python/LICENSE: LICENSE
	cp -a $< $@

python/README.rst: README.html
	cat $< | pandoc --from=html --to=rst --output=$@

python/dist: python/LICENSE python/README.rst
	cd python && python setup.py sdist
