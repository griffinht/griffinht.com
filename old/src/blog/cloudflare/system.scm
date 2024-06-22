(use-modules (gnu bootloader)
             (gnu bootloader grub)
             (gnu system file-systems)
             (gnu services base)
             (gnu services ssh)
             (gnu packages certs)
             (guix gexp)
             (gnu system))

(operating-system
  (host-name "test")
  (bootloader (bootloader-configuration (bootloader grub-bootloader)))
  (file-systems %base-file-systems)
  (packages (cons nss-certs %base-packages))
  (services 
    (list
      ; note getaddrinfo thing doesn't work without /etc/services lol todo fix this maybe?
      ;(service urandom-seed-service-type) ; needed to generate entropy to generate the key pair, otherwise system won't really boot (but will be functional)
        (service guix-service-type
                                            (guix-configuration
                                              (substitute-urls
                                                (append (list "https://guix.griffinht.com")
                                                        %default-substitute-urls)))))))
