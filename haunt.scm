(use-modules (haunt asset)
             (haunt site)
             (haunt builder blog)
             (haunt builder atom)
             (haunt reader skribe))

(site #:title "my first site"
      #:domain "griffinht.com"
      #:default-metadata
      '((author . "your mom"))
      #:readerss (list skribe-reader)
      #:builders (list (blog)
                       (atom-feed)
                       (atom-feeds-by-tag)))
