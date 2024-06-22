.DELETE_ON_ERROR:

rss.xml: $(wildcard src/blog/*.md)
	pandoc-rss \
		-t "griffin's blog" \
		-d 'this is my blog' \
		-l 'https://griffinht.com/blog' \
		-n 'en-US' \
		-w 'blog@griffinht.com (Griffin Tomaszewski)' \
		-s \
		$^ > '$@'

BUILD=build

$(BUILD).%:
	./build.sh '$*' src $(BUILD)

$(BUILD): build.build src
	touch '$@'

watch: build.watch

serve.dumb: $(BUILD)
	@echo -e '\n\n\n'
	python3 -m http.server --directory '$<'

serve: $(BUILD)
	@echo -e '\n\n\n'
	livereload '$<'

upload: $(BUILD)
	wrangler pages deploy \
		'$<' #--branch=master

deploy: $(BUILD)
	wrangler pages deploy \
		'$<' \
		--branch=dev
clean:
	rm -fr $(BUILD)
