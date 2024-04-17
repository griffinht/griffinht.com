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

