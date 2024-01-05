(use-modules (gnu))
(operating-system
  (host-name "test")
  ; ignored
  (bootloader (bootloader-configuration
                (bootloader grub-bootloader)))
  ; ignored
  (file-systems %base-file-systems)
  (services 
    (cons
        (service openssh-service-type
                 (openssh-configuration
                   (permit-root-login 'prohibit-password)
                   (authorized-keys
                     `(("root" ,(local-file "id_ed25519.pub"))))))
        (modify-services %base-services
                         (guix-service-type config =>
                                            (guix-configuration
                                              (inherit config)
                                              (substitute-urls
                                                (append (list "https://guix.griffinht.com")
                                                        %default-substitute-urls))))))))
