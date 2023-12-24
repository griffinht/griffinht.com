# Installing Linux the Guix way

Guix allows 

```scheme
(operating-system
  (host-name "my-system")
  (bootloader (bootloader-configuration
                (bootloader grub-bootloader)))
```
