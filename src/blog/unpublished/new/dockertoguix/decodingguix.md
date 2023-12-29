todo find other blogs which do this

guix shell python python-chevron python-markdown python-pyyaml

What makes up a Guix package?

Let's pack up everything that comprises `python` package as a compressed tarball:

```bash
$ tar -xz < "$(guix pack python)"
$ ls
gnu
$ tree -L 3 gnu
gnu
└── store
    ├── 0lm4jxcmzxfdn95y28d3y3axp85jnnn3-tcl-8.6.12
    │   ├── bin
    │   ├── etc
    │   ├── include
    │   ├── lib
    │   └── share
    ├── 1fjm5sqgiwl2rcy9fwn69abaahx6z3sq-ncurses-6.2.20210619
    │   ├── bin
    │   ├── etc
    │   ├── include
    │   ├── lib
    │   └── share
    ├── 1i83gaifl3bmsx5j9k4h90ydwkfm18jf-libpng-1.6.37
    │   ├── bin
    │   ├── etc
    │   ├── include
    │   ├── lib
    │   └── share
    ├── 21g9zdpgvnfvf36z16k0badjv0mg1shh-libxft-2.3.4
    │   ├── include
    │   ├── lib
    │   └── share
    ├── 31cgfs6dwhlv5hmcx6wgrqh2lkxnfpps-bzip2-1.0.8
    │   ├── bin
    │   ├── etc
    │   ├── include
    │   ├── lib
    │   └── share
    ├── 6ncav55lbk5kqvwwflrzcr41hp5jbq0c-gcc-11.3.0-lib
    │   ├── include
    │   ├── lib
    │   └── share
    ├── 94rdaacvsqf05zhw88w92y8bkvgxdfpl-expat-2.5.0
    │   ├── bin
    │   ├── etc
    │   ├── include
    │   ├── lib
    │   └── share
    ├── d6v343l5328yg64dmw7ww4sw4f2pr8va-libx11-1.8.7
    │   ├── include
    │   ├── lib
    │   └── share
    ├── g34irq2wzd6m3sjw4yvwyg70vd78nm5g-emacs-subdirs
    │   └── share
    ├── h855kddqbay0pcbwr8a7i8m6ilz67cfn-python-3.10.7
    │   ├── bin
    │   ├── etc
    │   ├── include
    │   ├── lib
    │   └── share
    ├── hl6lb3irs8wrfv49fnirxshsq590pi9v-zlib-1.2.13
    │   ├── include
    │   ├── lib
    │   └── share
    ├── j2flhwg0sm59blypg3wdc6d4crdzj3rh-freetype-2.13.0
    │   ├── bin
    │   ├── include
    │   ├── lib
    │   └── share
    ├── ka0rng7n5bmxprppshpqhmkzf8hx8nq9-libxcb-1.15
    │   ├── include
    │   ├── lib
    │   └── share
    ├── kl7vp2gvcp2f2r2xrsiyzcvl794wz6sh-openssl-3.0.8
    │   ├── bin
    │   ├── etc
    │   ├── include
    │   ├── lib
    │   └── share
    ├── l0y8jkmip7qpa7x33972mn0dsfy8ac01-libffi-3.4.4
    │   ├── include
    │   ├── lib
    │   └── share
    ├── ln6hxqjvz6m9gdd9s97pivlqck7hzs99-glibc-2.35
    │   ├── bin
    │   ├── etc
    │   ├── include
    │   ├── lib
    │   ├── libexec
    │   ├── sbin
    │   ├── share
    │   └── var
    ├── m3x2smrp3f86yxk98nkqy3vg86r6airb-profile
    │   ├── bin -> /gnu/store/h855kddqbay0pcbwr8a7i8m6ilz67cfn-python-3.10.7/bin
    │   ├── etc
    │   ├── include -> /gnu/store/h855kddqbay0pcbwr8a7i8m6ilz67cfn-python-3.10.7/include
    │   ├── lib -> /gnu/store/h855kddqbay0pcbwr8a7i8m6ilz67cfn-python-3.10.7/lib
    │   ├── manifest
    │   └── share
    ├── mcllmdn8li69sacc0cciqrb3lyz35haz-sqlite-3.39.3
    │   ├── bin
    │   ├── etc
    │   ├── include
    │   ├── lib
    │   └── share
    ├── nigj1sqxh39ghqpwx5chrkf14h8iwpnq-fontconfig-minimal-2.14.0
    │   ├── bin
    │   ├── etc
    │   ├── include
    │   ├── lib
    │   └── share
    ├── p425d7r839x9f3w0kl7rf4cd516a3ag4-libxau-1.0.10
    │   ├── include
    │   ├── lib
    │   └── share
    ├── q8p6b4yikc9g368qfja859f7531wnvwa-tk-8.6.12
    │   ├── bin
    │   ├── etc
    │   ├── include
    │   ├── lib
    │   └── share
    ├── rg3fzmw1l4ljqgjq4vq9j3a7v199mzwy-xz-5.2.8
    │   ├── bin
    │   ├── etc
    │   ├── include
    │   ├── lib
    │   └── share
    ├── rkqkby3dxsvdnijcbh7rlbz71p7hv3mq-libxrender-0.9.10
    │   ├── include
    │   ├── lib
    │   └── share
    ├── v1znwwy207bfmpq0gb40xj3zaah4kbwv-info-dir
    │   └── share
    ├── v9p25q9l5nnaixkhpap5rnymmwbhf9rp-bash-minimal-5.1.16
    │   ├── bin
    │   ├── etc
    │   └── share
    ├── xkr1i02q2j0j0l8hksbnh9kcrdrizyk4-readline-8.1.2
    │   ├── bin
    │   ├── include
    │   ├── lib
    │   └── share
    ├── xwwisbnpbg73wzh9rfmghm51i1k32030-bzip2-1.0.8
    │   ├── bin
    │   ├── etc
    │   ├── include
    │   ├── lib
    │   └── share
    ├── z60r50m2crx3qlha1k4ciywidyl1x5r9-libxdmcp-1.1.3
    │   ├── include
    │   ├── lib
    │   └── share
    ├── z655ilai81pbzbm35zwfqc64ha7wl37k-gdbm-1.23
    │   ├── bin
    │   ├── etc
    │   ├── include
    │   ├── lib
    │   └── share
    ├── zan3d655r50cv5gxvj2l5yybwhy6x3n4-font-dejavu-2.37
    │   └── share
    └── zzyywykw7kriln18rxqd82f0k5kidla7-bash-static-5.1.16
        ├── bin
        └── share

154 directories, 1 file
```

`guix size` [manual](https://guix.gnu.org/manual/en/html_node/Invoking-guix-size.html) helps us profile the disk usage of these packages.

```bash
$ guix size python
store item                                                       total    self
/gnu/store/91wasjkmy50p8fq0rf9jby80mnmq1fxr-python-3.10.7          226.3    74.0  32.7%
/gnu/store/gsjczqir1wbz8p770zndrpw4rnppmxi3-glibc-2.35              40.6    38.8  17.1%
/gnu/store/930nwsiysdvy2x5zv1sf6v7ym75z8ayk-gcc-11.3.0-lib          75.3    34.7  15.3%
/gnu/store/gqsxab8w881ds9raxkv74k0xcjds3z10-tcl-8.6.12             102.0    25.7  11.3%
/gnu/store/zan3d655r50cv5gxvj2l5yybwhy6x3n4-font-dejavu-2.37         9.8     9.8   4.3%
/gnu/store/vzl3lmb1lh702wvb3l1b3dzs2391lp02-tk-8.6.12              130.8     8.4   3.7%
/gnu/store/69wd3pd1hd3j84xr965jj2fk2qmxn0hl-openssl-3.0.8           83.4     8.1   3.6%
/gnu/store/bcc053jvsbspdjr17gnnd9dg85b3a0gy-ncurses-6.2.20210619    81.2     5.9   2.6%
/gnu/store/4jakqiibsvrkv4jdw1wyl6racrwv9bkh-sqlite-3.39.3           86.0     3.4   1.5%
/gnu/store/qabydd2r26gcr9s26hzchip3a3h3zhg4-libxcb-1.15             78.5     3.0   1.3%
/gnu/store/h0psmmlgczv2lpspz058p3gsnw96xxz6-libx11-1.8.7            81.2     2.7   1.2%
/gnu/store/3dv9xf07gnmc4gpm0a4h0g7j58dx3l05-freetype-2.13.0         79.9     2.5   1.1%
/gnu/store/zzyywykw7kriln18rxqd82f0k5kidla7-bash-static-5.1.16       1.8     1.8   0.8%
/gnu/store/lxfc2a05ysi7vlaq0m3w5wsfsy0drdlw-readline-8.1.2          82.6     1.4   0.6%
/gnu/store/6k1yys9wqrfn4y41ic1win8gpnimncwj-xz-5.2.8                77.7     1.4   0.6%
/gnu/store/rib9g2ig1xf3kclyl076w28parmncg4k-bash-minimal-5.1.16     41.6     1.0   0.4%
/gnu/store/2w976k6g70gkfih9wwhalqsni209vcqz-gdbm-1.23               75.9     0.6   0.3%
/gnu/store/fncsrwapajvfkl76zmn6z1cxqd7hlbqf-fontconfig-minimal-2.14.0    90.7     0.6   0.3%
/gnu/store/zkxvwia0z25409k1kmm0jqzfk9prc8fx-libpng-1.6.37           77.1     0.5   0.2%
/gnu/store/pl09vk5g3cl8fxfln2hjk996pyahqk8m-bzip2-1.0.8             76.7     0.4   0.2%
/gnu/store/j8wlfmlmfvpbza6is9wv9xsd8psrxn00-bzip2-1.0.8             76.7     0.4   0.2%
/gnu/store/fw1wywd34vh33l4dq182ds5d7jdz45j5-expat-2.5.0             75.7     0.4   0.2%
/gnu/store/slzq3zqwj75lbrg4ly51hfhbv2vhryv5-zlib-1.2.13             75.5     0.2   0.1%
/gnu/store/w8b0l8hk6g0fahj4fvmc4qqm3cvaxnmv-libffi-3.4.4            75.5     0.2   0.1%
/gnu/store/xkzw5shd6bchzvhv9d6p08hsny749jdd-libxdmcp-1.1.3          75.4     0.1   0.1%
/gnu/store/1xk89253r6kkqbvpvpdla1gggc1gnj37-libxft-2.3.4            96.7     0.1   0.1%
/gnu/store/hvqgs2pqadj2zwif12pp71yjgd7kfd0n-libxrender-0.9.10       81.2     0.1   0.0%
/gnu/store/yilf64y14qciml3kkj3506i3n2gmaawb-libxau-1.0.10           75.3     0.0   0.0%
total: 226.3 MiB
```

That's a lot of stuff. Let's pick a random package and see how big it is by itself:

```bash
$ guix size sqlite
store item                                                       total    self
/gnu/store/gsjczqir1wbz8p770zndrpw4rnppmxi3-glibc-2.35              40.6    38.8  45.0%
/gnu/store/930nwsiysdvy2x5zv1sf6v7ym75z8ayk-gcc-11.3.0-lib          75.3    34.7  40.3%
/gnu/store/bcc053jvsbspdjr17gnnd9dg85b3a0gy-ncurses-6.2.20210619    81.2     5.9   6.9%
/gnu/store/i17mvp84jhfs87k695ldr8djxcn6hrv7-sqlite-3.42.0           86.1     3.5   4.0%
/gnu/store/zzyywykw7kriln18rxqd82f0k5kidla7-bash-static-5.1.16       1.8     1.8   2.1%
/gnu/store/lxfc2a05ysi7vlaq0m3w5wsfsy0drdlw-readline-8.1.2          82.6     1.4   1.6%
total: 86.1 MiB
```

Why is `sqlite` in here? Let's check with `guix graph` [manual](https://guix.gnu.org/manual/en/html_node/Invoking-guix-graph.html)

```bash
$ guix size python
kkk
```

todo transitive deps make it smaller overall


Let's compare this to the official Python Docker image.
Actually, the Python Docker image also has pip - let's add that to ours.

```bash
$ guix shell python python-pip
```

Know any other neat tricks for inspecting Guix packages? Let me know! todo email?
