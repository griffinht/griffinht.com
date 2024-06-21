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

buildd:
	rm -fr build
	set -e && find src | while read -r file; do ./build2.sh $(PWD)/src "$(PWD)/$$file"; done
	echo initial build complete
	find src | WATCH=true entr ./build2.sh $(PWD)/src /_

serve:
	echo http://localhost:8000
	python3 -m http.server --directory build
