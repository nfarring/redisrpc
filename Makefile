TARGETS:=\
    composer.phar\
    php/vendor\
    python/LICENSE\
    python/README.rst\
    python/MANIFEST\
    python/dist

.PHONY: all
all: $(TARGETS)

.PHONY: clean
clean:
	rm -rf $(TARGETS) python/build

composer.phar:
	curl -s http://getcomposer.org/installer | php

php/vendor: composer.phar
	php composer.phar install

python/LICENSE: LICENSE
	cp -a $< $@

# Ref: https://github.com/alampros/Docter
python/README.rst: README.markdown
	~/bin/github-flavored-markdown.rb $< | pandoc --from=html --to=rst --output=$@

python/MANIFEST python/dist: python/LICENSE python/README.rst
	cd python && python setup.py sdist
