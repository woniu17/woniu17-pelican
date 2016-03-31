Title: QUIC编译环境搭建
Date: 2016-03-30 15:08
Category: Protocol
Tags: Protocol, QUIC
Slug: QUIC build environment
Author: qingluck
Summary: build environment for QUIC.
Comment: off

### 注意事项
* 以下步骤大部分都需要搭梯子
* chromium/src/build/install-build-deps.sh只支持Ubuntu 12.04, 14.04, 14.10, 15.04, 15.10
* 在32位系统使用命令*ninja -C out/Debug quic_server quic_client*会出现错误[a][1]
* 在Ubuntu 14.04(64 bit)执行**./build/install-build-deps.sh**时出现很多依赖无法解决问题

综上几点，建议使用**Ubuntu 12.04(64 bit)**

### 克隆并安装depot_tools
将代码库克隆到本地
```bash
$ git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git
```
将depot_tools添加到PATH变量
```bash
$ export PATH=$PATH:/path/to/depot_tools
```
### 将chromium代码克隆下来（约有15GB）
```bash
$ mkdir chromium && cd chromium
$ fetch --nohooks chromium     # Optionally, --no-history
```
如果上述fetch命令卡住（chromium大小长时间不再增加），可停止fetch命令，重新使用一下命令继续：
```bash
$ gclient sync --nohooks
```

### 安装必要依赖
```bash
$ cd src
$ ./build/install-build-deps.sh --no-chromeos-fonts
$ cd ..
```
注：查看install-build-deps.sh可知安装的依赖包括[b]（可能不全），可使用**apt-get install**命令安装。

### 运行post-sync hooks
调用gyp生成平台相关的文件，保证后续编译通过。[2]
```bash
$ gclient runhooks
```

### 编译生成quic可运行服务端和客户端
```bash
$ ninja -C out/Debug quic_server quic_client
```

### 下载 www.example.org ，利用quic_server来服务
**注意**： www.example.org 是确实可访问的网址，不可以是其它网址，如 www.google.com 或 www.baidu.com 会产生认证问题
```bash
$ mkdir ~/tmp/quic-data
$ cd ~/tmp/quic-data
$ wget -p --save-headers https://www.example.org
$ vi www.example.org/index.html
$ cd -
```
### 编辑~/tmp/quic-data/www.example.org/index.html
* 删除“Transfer-Encoding: chunked”这一行
* 删除“Alternate-Protocol: ...”这一行
* 添加一行“X-Original-Url: https://www.example.org/”（不包括双引号）

### 生成加密证书
```bash
$ cd net/tools/quic/certs
$ ./generate-certs.sh
$ cd -
```

### 安装CA证书（安装于quic_client机子上）
```bash
$ sudo apt-get install libnss3-tools
$ certutil -d sql:$HOME/.pki/nssdb -A -t "C,," -n "QUIC CA" -i net/tools/quic/certs/out/2048-sha256-root.pem
$ certutil -d sql:$HOME/.pki/nssdb -L
```
如果要删除QUIC CA证书，使用```certutil -d sql:$HOME/.pki/nssdb -D -n "QUIC CA"```
**确保变量$HOME值为当前用户的主目录**
看到以下输出，确定QUIC CA证书已安装
>Certificate Nickname                                         Trust Attributes
>                                                             SSL,S/MIME,JAR/XPI
>
>QUIC CA                                                      C,,

### 运行quic_server
```bash
$ ./out/Debug/quic_server \
  --quic_in_memory_cache_dir=$HOME/tmp/quic-data/www.example.org \
  --certificate_file=net/tools/quic/certs/out/leaf_cert.pem \
  --key_file=net/tools/quic/certs/out/leaf_cert.pkcs8 --v=1
```
***注意***：上述命令不可以将$HOME更改为"~"
### 运行quic_client
```bash
$ ./out/Debug/quic_client --host=127.0.0.1 --port=6121 https://www.example.org/ --v=1
```

[1] [https://groups.google.com/forum/#!topic/discuss-webrtc/bq7zgQRC6fc](https://groups.google.com/forum/#!topic/discuss-webrtc/bq7zgQRC6fc)
[2] [http://blog.csdn.net/jaylinzhou/article/details/9012993](http://blog.csdn.net/jaylinzhou/article/details/9012993)

[a] 在32位使用命令*ninja -C out/Debug quic_server quic_client*出现以下错误
>FAILED: ../../third_party/llvm-build/Release+Asserts/bin/clang -MMD -MF obj/third_party/zlib/zlib.deflate.o.d -DV8_DEPRECATION_WARNINGS -DCLD_VERSION=2 -D_FILE_OFFSET_BITS=64 -DCHROMIUM_BUILD -DCR_CLANG_REVISION=263324-1 -DUI_COMPOSITOR_IMAGE_TRANSPORT -DUSE_AURA=1 -DUSE_PANGO=1 -DUSE_CAIRO=1 -DUSE_DEFAULT_RENDER_THEME=1 -DUSE_LIBJPEG_TURBO=1 -DUSE_X11=1 -DUSE_CLIPBOARD_AURAX11=1 -DENABLE_WEBRTC=1 -DENABLE_MEDIA_ROUTER=1 -DENABLE_PEPPER_CDMS -DENABLE_CONFIGURATION_POLICY -DENABLE_NOTIFICATIONS -DENABLE_TOPCHROME_MD=1 -DUSE_UDEV -DFIELDTRIAL_TESTING_ENABLED -DENABLE_TASK_MANAGER=1 -DENABLE_EXTENSIONS=1 -DENABLE_PDF=1 -DENABLE_PLUGINS=1 -DENABLE_SESSION_SERVICE=1 -DENABLE_THEMES=1 -DENABLE_AUTOFILL_DIALOG=1 -DENABLE_PRINTING=1 -DENABLE_BASIC_PRINTING=1 -DENABLE_PRINT_PREVIEW=1 -DENABLE_SPELLCHECK=1 -DENABLE_CAPTIVE_PORTAL_DETECTION=1 -DENABLE_APP_LIST=1 -DENABLE_SETTINGS_APP=1 -DENABLE_SUPERVISED_USERS=1 -DENABLE_MDNS=1 -DENABLE_SERVICE_DISCOVERY=1 -DV8_USE_EXTERNAL_STARTUP_DATA -DFULL_SAFE_BROWSING -DSAFE_BROWSING_CSD -DSAFE_BROWSING_DB_LOCAL -DUSE_LIBPCI=1 -DUSE_OPENSSL=1 -DUSE_GLIB=1 -DUSE_NSS_CERTS=1 -DUSE_NSS_VERIFIER=1 -DDYNAMIC_ANNOTATIONS_ENABLED=1 -DWTF_USE_DYNAMIC_ANNOTATIONS=1 -D_DEBUG -Igen -I../../third_party/zlib -fstack-protector --param=ssp-buffer-size=4 -Werror -pthread -fno-strict-aliasing -Wall -Wno-unused-parameter -Wno-missing-field-initializers -fvisibility=hidden -pipe -fPIC -Xclang -load -Xclang /home/lqx/code/chromium/src/third_party/llvm-build/Release+Asserts/lib/libFindBadConstructs.so -Xclang -add-plugin -Xclang find-bad-constructs -Xclang -plugin-arg-find-bad-constructs -Xclang check-templates -Xclang -plugin-arg-find-bad-constructs -Xclang follow-macro-expansion -momit-leaf-frame-pointer -mstack-alignment=16 -mstackrealign -fcolor-diagnostics -B/home/lqx/code/chromium/src/third_party/binutils/Linux_x64/Release/bin -Wheader-hygiene -Wno-char-subscripts -Wno-unneeded-internal-declaration -Wno-covered-switch-default -Wstring-conversion -Wno-c++11-narrowing -Wno-deprecated-register -Wno-inconsistent-missing-override -Wno-shift-negative-value -Wno-incompatible-pointer-types -Wno-unused-variable -msse2 -mfpmath=sse -mmmx -m32 --sysroot=/home/lqx/code/chromium/src/build/linux/debian_wheezy_i386-sysroot -O0 -g -funwind-tables   -c ../../third_party/zlib/deflate.c -o obj/third_party/zlib/zlib.deflate.o
../../third_party/llvm-build/Release+Asserts/bin/clang: 1: ../../third_party/llvm-build/Release+Asserts/bin/clang: Syntax error: "(" unexpected
[2/1821] CC obj/third_party/zlib/zlib.gzlib.o
>FAILED: ../../third_party/llvm-build/Release+Asserts/bin/clang -MMD -MF obj/third_party/zlib/zlib.gzlib.o.d -DV8_DEPRECATION_WARNINGS -DCLD_VERSION=2 -D_FILE_OFFSET_BITS=64 -DCHROMIUM_BUILD -DCR_CLANG_REVISION=263324-1 -DUI_COMPOSITOR_IMAGE_TRANSPORT -DUSE_AURA=1 -DUSE_PANGO=1 -DUSE_CAIRO=1 -DUSE_DEFAULT_RENDER_THEME=1 -DUSE_LIBJPEG_TURBO=1 -DUSE_X11=1 -DUSE_CLIPBOARD_AURAX11=1 -DENABLE_WEBRTC=1 -DENABLE_MEDIA_ROUTER=1 -DENABLE_PEPPER_CDMS -DENABLE_CONFIGURATION_POLICY -DENABLE_NOTIFICATIONS -DENABLE_TOPCHROME_MD=1 -DUSE_UDEV -DFIELDTRIAL_TESTING_ENABLED -DENABLE_TASK_MANAGER=1 -DENABLE_EXTENSIONS=1 -DENABLE_PDF=1 -DENABLE_PLUGINS=1 -DENABLE_SESSION_SERVICE=1 -DENABLE_THEMES=1 -DENABLE_AUTOFILL_DIALOG=1 -DENABLE_PRINTING=1 -DENABLE_BASIC_PRINTING=1 -DENABLE_PRINT_PREVIEW=1 -DENABLE_SPELLCHECK=1 -DENABLE_CAPTIVE_PORTAL_DETECTION=1 -DENABLE_APP_LIST=1 -DENABLE_SETTINGS_APP=1 -DENABLE_SUPERVISED_USERS=1 -DENABLE_MDNS=1 -DENABLE_SERVICE_DISCOVERY=1 -DV8_USE_EXTERNAL_STARTUP_DATA -DFULL_SAFE_BROWSING -DSAFE_BROWSING_CSD -DSAFE_BROWSING_DB_LOCAL -DUSE_LIBPCI=1 -DUSE_OPENSSL=1 -DUSE_GLIB=1 -DUSE_NSS_CERTS=1 -DUSE_NSS_VERIFIER=1 -DDYNAMIC_ANNOTATIONS_ENABLED=1 -DWTF_USE_DYNAMIC_ANNOTATIONS=1 -D_DEBUG -Igen -I../../third_party/zlib -fstack-protector --param=ssp-buffer-size=4 -Werror -pthread -fno-strict-aliasing -Wall -Wno-unused-parameter -Wno-missing-field-initializers -fvisibility=hidden -pipe -fPIC -Xclang -load -Xclang /home/lqx/code/chromium/src/third_party/llvm-build/Release+Asserts/lib/libFindBadConstructs.so -Xclang -add-plugin -Xclang find-bad-constructs -Xclang -plugin-arg-find-bad-constructs -Xclang check-templates -Xclang -plugin-arg-find-bad-constructs -Xclang follow-macro-expansion -momit-leaf-frame-pointer -mstack-alignment=16 -mstackrealign -fcolor-diagnostics -B/home/lqx/code/chromium/src/third_party/binutils/Linux_x64/Release/bin -Wheader-hygiene -Wno-char-subscripts -Wno-unneeded-internal-declaration -Wno-covered-switch-default -Wstring-conversion -Wno-c++11-narrowing -Wno-deprecated-register -Wno-inconsistent-missing-override -Wno-shift-negative-value -Wno-incompatible-pointer-types -Wno-unused-variable -msse2 -mfpmath=sse -mmmx -m32 --sysroot=/home/lqx/code/chromium/src/build/linux/debian_wheezy_i386-sysroot -O0 -g -funwind-tables   -c ../../third_party/zlib/gzlib.c -o obj/third_party/zlib/zlib.gzlib.o
../../third_party/llvm-build/Release+Asserts/bin/clang: 1: ../../third_party/llvm-build/Release+Asserts/bin/clang: Syntax error: "(" unexpected
ninja: build stopped: subcommand failed.

[b] install-build-deps.sh指出的所需依赖
>bison cdbs curl dpkg-dev elfutils devscripts fakeroot \
flex fonts-thai-tlwg g++ git-core git-svn gperf language-pack-da \
language-pack-fr language-pack-he language-pack-zh-hant \
libapache2-mod-php5 libasound2-dev libbrlapi-dev libav-tools \
libbz2-dev libcairo2-dev libcap-dev libcups2-dev libcurl4-gnutls-dev \
libdrm-dev libelf-dev libffi-dev libgconf2-dev libglib2.0-dev \
libglu1-mesa-dev libgnome-keyring-dev libgtk2.0-dev libkrb5-dev \
libnspr4-dev libnss3-dev libpam0g-dev libpci-dev libpulse-dev \
libsctp-dev libspeechd-dev libsqlite3-dev libssl-dev libudev-dev \
libwww-perl libxslt1-dev libxss-dev libxt-dev libxtst-dev openbox \
patch perl php5-cgi pkg-config python python-cherrypy3 python-crypto \
python-dev python-numpy python-opencv python-openssl python-psutil \
python-yaml rpm ruby subversion ttf-dejavu-core ttf-indic-fonts \
ttf-kochi-gothic ttf-kochi-mincho wdiff zip

[c] 运行命令***./build/install-build-deps.sh  --no-chromeos-fonts***打印的日志，前期已经使用命令**apt-get install**安装过[b]中的依赖

>lqx@bogon:~/code/chromium$ proxychains src/build/install-build-deps.sh  --no-chromeos-fonts
ProxyChains-3.1 (http://proxychains.sf.net)
Running as non-root user.
You might have to enter your password one or more times for 'sudo'.

>This script installs all tools and libraries needed to build Chromium.

>For most of the libraries, it can also install debugging symbols, which
will allow you to debug code in the system libraries. Most developers
won't need these symbols.
Do you want me to install them for you (y/N) N
Skipping debugging symbols.
Including 32-bit libraries for ARM/Android.
Including ARM cross toolchain.
Including NaCl, NaCl toolchain, NaCl ports dependencies.
ERROR: ld.so: object 'libproxychains.so.3' from LD_PRELOAD cannot be preloaded: ignored.
Get:1 http://extras.ubuntu.com precise Release.gpg [72 B]
Hit http://security.ubuntu.com precise-security Release.gpg                                                     
Hit http://cn.archive.ubuntu.com precise Release.gpg                                           
Hit http://cn.archive.ubuntu.com precise-updates Release.gpg
Hit http://cn.archive.ubuntu.com precise-backports Release.gpg
Hit http://cn.archive.ubuntu.com precise Release
Hit http://cn.archive.ubuntu.com precise-updates Release                                    
Hit http://cn.archive.ubuntu.com precise-backports Release                                  
Hit http://cn.archive.ubuntu.com precise/main Sources                                       
Hit http://extras.ubuntu.com precise Release                         
Err http://extras.ubuntu.com precise Release                          
  
>Hit http://cn.archive.ubuntu.com precise/restricted Sources           
Hit http://security.ubuntu.com precise-security Release
Hit http://security.ubuntu.com precise-security/main Sources
Hit http://cn.archive.ubuntu.com precise/universe Sources
Hit http://security.ubuntu.com precise-security/restricted Sources
Hit http://security.ubuntu.com precise-security/universe Sources
Hit http://security.ubuntu.com precise-security/multiverse Sources
Hit http://security.ubuntu.com precise-security/main amd64 Packages
Hit http://security.ubuntu.com precise-security/restricted amd64 Packages
Hit http://security.ubuntu.com precise-security/universe amd64 Packages
Hit http://security.ubuntu.com precise-security/multiverse amd64 Packages
Hit http://security.ubuntu.com precise-security/main i386 Packages
Hit http://security.ubuntu.com precise-security/restricted i386 Packages
Hit http://security.ubuntu.com precise-security/universe i386 Packages
Hit http://security.ubuntu.com precise-security/multiverse i386 Packages
Hit http://cn.archive.ubuntu.com precise/multiverse Sources
Hit http://cn.archive.ubuntu.com precise/main amd64 Packages
Hit http://cn.archive.ubuntu.com precise/restricted amd64 Packages
Hit http://cn.archive.ubuntu.com precise/universe amd64 Packages
Hit http://security.ubuntu.com precise-security/main TranslationIndex
Hit http://cn.archive.ubuntu.com precise/multiverse amd64 Packages
Hit http://cn.archive.ubuntu.com precise/main i386 Packages
Hit http://cn.archive.ubuntu.com precise/restricted i386 Packages
Hit http://cn.archive.ubuntu.com precise/universe i386 Packages
Hit http://cn.archive.ubuntu.com precise/multiverse i386 Packages
Hit http://cn.archive.ubuntu.com precise/main TranslationIndex
Hit http://security.ubuntu.com precise-security/multiverse TranslationIndex
Hit http://cn.archive.ubuntu.com precise/multiverse TranslationIndex
Hit http://security.ubuntu.com precise-security/restricted TranslationIndex
Hit http://cn.archive.ubuntu.com precise/restricted TranslationIndex
Hit http://cn.archive.ubuntu.com precise/universe TranslationIndex
Hit http://cn.archive.ubuntu.com precise-updates/main Sources
Hit http://cn.archive.ubuntu.com precise-updates/restricted Sources
Hit http://cn.archive.ubuntu.com precise-updates/universe Sources
Hit http://security.ubuntu.com precise-security/universe TranslationIndex
Hit http://security.ubuntu.com precise-security/main Translation-en
Hit http://security.ubuntu.com precise-security/multiverse Translation-en    
Hit http://security.ubuntu.com precise-security/restricted Translation-en    
Hit http://security.ubuntu.com precise-security/universe Translation-en      
Hit http://cn.archive.ubuntu.com precise-updates/multiverse Sources
Hit http://cn.archive.ubuntu.com precise-updates/main amd64 Packages
Hit http://cn.archive.ubuntu.com precise-updates/restricted amd64 Packages
Hit http://cn.archive.ubuntu.com precise-updates/universe amd64 Packages
Hit http://cn.archive.ubuntu.com precise-updates/multiverse amd64 Packages
Hit http://cn.archive.ubuntu.com precise-updates/main i386 Packages
Hit http://cn.archive.ubuntu.com precise-updates/restricted i386 Packages
Hit http://cn.archive.ubuntu.com precise-updates/universe i386 Packages
Hit http://cn.archive.ubuntu.com precise-updates/multiverse i386 Packages
Hit http://cn.archive.ubuntu.com precise-updates/main TranslationIndex
Hit http://cn.archive.ubuntu.com precise-updates/multiverse TranslationIndex
Hit http://cn.archive.ubuntu.com precise-updates/restricted TranslationIndex
Hit http://cn.archive.ubuntu.com precise-updates/universe TranslationIndex
Hit http://cn.archive.ubuntu.com precise-backports/main Sources
Hit http://cn.archive.ubuntu.com precise-backports/restricted Sources
Hit http://cn.archive.ubuntu.com precise-backports/universe Sources
Hit http://cn.archive.ubuntu.com precise-backports/multiverse Sources
Hit http://cn.archive.ubuntu.com precise-backports/main amd64 Packages
Hit http://cn.archive.ubuntu.com precise-backports/restricted amd64 Packages
Hit http://cn.archive.ubuntu.com precise-backports/universe amd64 Packages
Hit http://cn.archive.ubuntu.com precise-backports/multiverse amd64 Packages
Hit http://cn.archive.ubuntu.com precise-backports/main i386 Packages
Hit http://cn.archive.ubuntu.com precise-backports/restricted i386 Packages
Hit http://cn.archive.ubuntu.com precise-backports/universe i386 Packages
Hit http://cn.archive.ubuntu.com precise-backports/multiverse i386 Packages
Hit http://cn.archive.ubuntu.com precise-backports/main TranslationIndex
Hit http://cn.archive.ubuntu.com precise-backports/multiverse TranslationIndex
Hit http://cn.archive.ubuntu.com precise-backports/restricted TranslationIndex
Hit http://cn.archive.ubuntu.com precise-backports/universe TranslationIndex
Hit http://cn.archive.ubuntu.com precise/main Translation-en
Hit http://cn.archive.ubuntu.com precise/multiverse Translation-en
Hit http://cn.archive.ubuntu.com precise/restricted Translation-en
Hit http://cn.archive.ubuntu.com precise/universe Translation-en
Hit http://cn.archive.ubuntu.com precise-updates/main Translation-en
Hit http://cn.archive.ubuntu.com precise-updates/multiverse Translation-en
Hit http://cn.archive.ubuntu.com precise-updates/restricted Translation-en
Hit http://cn.archive.ubuntu.com precise-updates/universe Translation-en
Hit http://cn.archive.ubuntu.com precise-backports/main Translation-en
Hit http://cn.archive.ubuntu.com precise-backports/multiverse Translation-en
Hit http://cn.archive.ubuntu.com precise-backports/restricted Translation-en
Hit http://cn.archive.ubuntu.com precise-backports/universe Translation-en
Fetched 72 B in 4s (15 B/s)
Reading package lists... Done
W: A error occurred during the signature verification. The repository is not updated and the previous index files will be used. GPG error: http://extras.ubuntu.com precise Release: The following signatures were invalid: BADSIG 16126D3A3E5C1192 Ubuntu Extras Archive Automatic Signing Key <ftpmaster@ubuntu.com>

>W: Failed to fetch http://extras.ubuntu.com/ubuntu/dists/precise/Release  

>W: Some index files failed to download. They have been ignored, or old ones used instead.
Finding missing packages...
Packages required:  libasound2:i386 libcap2:i386 libelf-dev:i386 libfontconfig1:i386 libgconf-2-4:i386 libgl1-mesa-glx-lts-trusty:i386 libglib2.0-0:i386 libgpm2:i386 libgtk2.0-0:i386 libncurses5:i386 libnss3:i386 libpango1.0-0:i386 libssl1.0.0:i386 libtinfo-dev:i386 libudev0:i386 libxcomposite1:i386 libxcursor1:i386 libxdamage1:i386 libxi6:i386 libxrandr2:i386 libxss1:i386 libxtst6:i386 linux-libc-dev:i386 ant apache2.2-bin appmenu-gtk autoconf bison cdbs cmake curl devscripts dpkg-dev elfutils fakeroot flex fonts-stix fonts-thai-tlwg g++ g++-4.6-multilib g++-arm-linux-gnueabihf gawk git-core git-svn g++-mingw-w64-i686 gperf intltool language-pack-da language-pack-fr language-pack-he language-pack-zh-hant lib32gcc1 lib32ncurses5-dev lib32stdc++6 lib32z1-dev libapache2-mod-php5 libasound2 libasound2-dev libatk1.0-0 libav-tools libbluetooth-dev libbrlapi0.5 libbrlapi-dev libbz2-1.0 libbz2-dev libc6 libc6-dev-armhf-cross libc6-i386 libcairo2 libcairo2-dev libcap2 libcap-dev libcups2 libcups2-dev libcurl4-gnutls-dev libdrm-dev libelf-dev libexpat1 libffi6 libffi-dev libfontconfig1 libfreetype6 libgbm-dev-lts-trusty libgconf2-dev libgl1-mesa-dev-lts-trusty libgles2-mesa-dev-lts-trusty libglib2.0-0 libglib2.0-dev libglu1-mesa-dev libgnome-keyring0 libgnome-keyring-dev libgtk2.0-0 libgtk2.0-dev libjpeg-dev libkrb5-dev libnspr4 libnspr4-dev libnss3 libnss3-dev libpam0g libpam0g-dev libpango1.0-0 libpci3 libpci-dev libpcre3 libpixman-1-0 libpng12-0 libpulse0 libpulse-dev libsctp-dev libspeechd2 libspeechd-dev libsqlite3-0 libsqlite3-dev libssl-dev libstdc++6 libtinfo-dev libtool libudev0 libudev-dev libwww-perl libx11-6 libxau6 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxdmcp6 libxext6 libxfixes3 libxi6 libxinerama1 libxkbcommon-dev libxrandr2 libxrender1 libxslt1-dev libxss-dev libxt-dev libxtst6 libxtst-dev linux-libc-dev-armhf-cross mesa-common-dev-lts-trusty openbox patch perl php5-cgi pkg-config python python-cherrypy3 python-crypto python-dev python-numpy python-opencv python-openssl python-psutil python-yaml realpath rpm ruby subversion texinfo ttf-dejavu-core ttf-indic-fonts ttf-kochi-gothic ttf-kochi-mincho ttf-mscorefonts-installer wdiff xsltproc xutils-dev xvfb zip zlib1g

>ERROR: ld.so: object 'libproxychains.so.3' from LD_PRELOAD cannot be preloaded: ignored.
No missing packages, and the packages are up-to-date.

>Skipping installation of Chrome OS fonts.
Installing symbolic links for NaCl.
Creating link: /usr/lib/i386-linux-gnu/libcrypto.so
ERROR: ld.so: object 'libproxychains.so.3' from LD_PRELOAD cannot be preloaded: ignored.
Creating link: /usr/lib/i386-linux-gnu/libssl.so
ERROR: ld.so: object 'libproxychains.so.3' from LD_PRELOAD cannot be preloaded: ignored.

[d]  ***gclient runhooks***命令打出的日志
>lqx@bogon:~/code/chromium$ proxychains gclient runhooks
ProxyChains-3.1 (http://proxychains.sf.net)

>________ running '/usr/bin/python src/build/landmines.py' in '/home/lqx/code/chromium'

>________ running '/usr/bin/python src/tools/remove_stale_pyc_files.py src/android_webview/tools src/build/android src/gpu/gles2_conform_support src/infra src/ppapi src/printing src/third_party/catapult src/third_party/closure_compiler/build src/tools' in '/home/lqx/code/chromium'

>________ running '/usr/bin/python src/build/download_nacl_toolchains.py --mode nacl_core_sdk sync --extract' in '/home/lqx/code/chromium'
Hook '/usr/bin/python src/build/download_nacl_toolchains.py --mode nacl_core_sdk sync --extract' took 14.04 secs

>________ running '/usr/bin/python src/build/android/play_services/update.py download' in '/home/lqx/code/chromium'

>________ running '/usr/bin/python src/build/linux/sysroot_scripts/install-sysroot.py --running-as-hook' in '/home/lqx/code/chromium'
Installing Debian Wheezy amd64 root image: /home/lqx/code/chromium/src/build/linux/debian_wheezy_amd64-sysroot
Downloading https://commondatastorage.googleapis.com/chrome-linux-sysroot/toolchain/c52471d9dec240c8d0a88fa98aa1eefeee32e22f/debian_wheezy_amd64_sysroot.tgz
|DNS-request| commondatastorage.googleapis.com 
|S-chain|-<>-127.0.0.1:1080-<><>-4.2.2.2:53-<><>-OK
|DNS-response| commondatastorage.googleapis.com is 216.58.197.16
|S-chain|-<>-127.0.0.1:1080-<><>-216.58.197.16:443-<><>-OK
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 41.6M  100 41.6M    0     0  40629      0  0:17:55  0:17:55 --:--:-- 69228
Debian Wheezy i386 root image already up-to-date: /home/lqx/code/chromium/src/build/linux/debian_wheezy_i386-sysroot
Hook '/usr/bin/python src/build/linux/sysroot_scripts/install-sysroot.py --running-as-hook' took 1080.59 secs

>________ running '/usr/bin/python src/build/vs_toolchain.py update' in '/home/lqx/code/chromium'

>________ running '/usr/bin/python src/third_party/binutils/download.py' in '/home/lqx/code/chromium'
0> Downloading /home/lqx/code/chromium/src/third_party/binutils/Linux_x64/binutils.tar.bz2...
Success!
Downloading 1 files took 193.957958 second(s)
Downloading /home/lqx/code/chromium/src/third_party/binutils/Linux_x64/binutils.tar.bz2
Extracting /home/lqx/code/chromium/src/third_party/binutils/Linux_x64/binutils.tar.bz2
Hook '/usr/bin/python src/third_party/binutils/download.py' took 195.69 secs

>________ running '/usr/bin/python src/tools/clang/scripts/update.py --if-needed' in '/home/lqx/code/chromium'
Updating Clang to 263324-1...
Creating directory /home/lqx/code/chromium/src/third_party/llvm-build
Downloading prebuilt clang
Downloading https://commondatastorage.googleapis.com/chromium-browser-clang/Linux_x64/clang-263324-1.tgz |DNS-request| commondatastorage.googleapis.com 
|S-chain|-<>-127.0.0.1:1080-<><>-4.2.2.2:53-<><>-OK
|DNS-response| commondatastorage.googleapis.com is 216.58.197.176
|S-chain|-<>-127.0.0.1:1080-<><>-216.58.197.176:443-<><>-OK
.......... Done.
Creating directory /home/lqx/code/chromium/src/third_party/llvm-build/Release+Asserts
clang 263324-1 unpacked
Hook '/usr/bin/python src/tools/clang/scripts/update.py --if-needed' took 1188.49 secs

>________ running '/usr/bin/python src/build/util/lastchange.py -o src/build/util/LASTCHANGE' in '/home/lqx/code/chromium'

>________ running '/usr/bin/python src/build/util/lastchange.py --git-hash-only -s src/third_party/WebKit -o src/build/util/LASTCHANGE.blink' in '/home/lqx/code/chromium'

>________ running 'download_from_google_storage --no_resume --platform=win32 --no_auth --bucket chromium-gn -s src/buildtools/win/gn.exe.sha1' in '/home/lqx/code/chromium'
The current platform doesn't match "win32", skipping.

>________ running 'download_from_google_storage --no_resume --platform=darwin --no_auth --bucket chromium-gn -s src/buildtools/mac/gn.sha1' in '/home/lqx/code/chromium'
The current platform doesn't match "darwin", skipping.

>________ running 'download_from_google_storage --no_resume --platform=linux* --no_auth --bucket chromium-gn -s src/buildtools/linux64/gn.sha1' in '/home/lqx/code/chromium'
0> Downloading src/buildtools/linux64/gn...
Success!
Downloading 1 files took 56.979077 second(s)
Hook 'download_from_google_storage --no_resume '--platform=linux*' --no_auth --bucket chromium-gn -s src/buildtools/linux64/gn.sha1' took 57.05 secs

>________ running 'download_from_google_storage --no_resume --platform=win32 --no_auth --bucket chromium-clang-format -s src/buildtools/win/clang-format.exe.sha1' in '/home/lqx/code/chromium'
The current platform doesn't match "win32", skipping.

>________ running 'download_from_google_storage --no_resume --platform=darwin --no_auth --bucket chromium-clang-format -s src/buildtools/mac/clang-format.sha1' in '/home/lqx/code/chromium'
The current platform doesn't match "darwin", skipping.

>________ running 'download_from_google_storage --no_resume --platform=linux* --no_auth --bucket chromium-clang-format -s src/buildtools/linux64/clang-format.sha1' in '/home/lqx/code/chromium'
0> Downloading src/buildtools/linux64/clang-format...
Success!
Downloading 1 files took 53.984268 second(s)
Hook 'download_from_google_storage --no_resume '--platform=linux*' --no_auth --bucket chromium-clang-format -s src/buildtools/linux64/clang-format.sha1' took 54.05 secs

>________ running 'download_from_google_storage --no_resume --platform=darwin --no_auth --bucket chromium-libcpp -s src/third_party/libc++-static/libc++.a.sha1' in '/home/lqx/code/chromium'
The current platform doesn't match "darwin", skipping.

>________ running 'download_from_google_storage --no_resume --platform=win32 --no_auth --bucket chromium-luci -d src/tools/luci-go/win64' in '/home/lqx/code/chromium'
The current platform doesn't match "win32", skipping.

>________ running 'download_from_google_storage --no_resume --platform=darwin --no_auth --bucket chromium-luci -d src/tools/luci-go/mac64' in '/home/lqx/code/chromium'
The current platform doesn't match "darwin", skipping.

>________ running 'download_from_google_storage --no_resume --platform=linux* --no_auth --bucket chromium-luci -d src/tools/luci-go/linux64' in '/home/lqx/code/chromium'
0> Downloading src/tools/luci-go/linux64/isolate...
Success!
Downloading 1 files took 318.788569 second(s)
Hook 'download_from_google_storage --no_resume '--platform=linux*' --no_auth --bucket chromium-luci -d src/tools/luci-go/linux64' took 318.87 secs

>________ running 'download_from_google_storage --no_resume --platform=linux* --no_auth --bucket chromium-eu-strip -s src/build/linux/bin/eu-strip.sha1' in '/home/lqx/code/chromium'
0> Downloading src/build/linux/bin/eu-strip...
Success!
Downloading 1 files took 18.628765 second(s)
Hook 'download_from_google_storage --no_resume '--platform=linux*' --no_auth --bucket chromium-eu-strip -s src/build/linux/bin/eu-strip.sha1' took 18.70 secs

>________ running 'download_from_google_storage --no_resume --platform=win32 --no_auth --bucket chromium-drmemory -s src/third_party/drmemory/drmemory-windows-sfx.exe.sha1' in '/home/lqx/code/chromium'
The current platform doesn't match "win32", skipping.

>________ running '/usr/bin/python src/build/get_syzygy_binaries.py --output-dir=src/third_party/syzygy/binaries --revision=83261eadef4d3a6ac2e2b325a39e62c27b283aca --overwrite' in '/home/lqx/code/chromium'
INFO:get_syzygy_binaries.py:Output directory does not exist, skipping cleanup.

>________ running '/usr/bin/python src/build/get_syzygy_binaries.py --output-dir=src/third_party/kasko/binaries --revision=266a18d9209be5ca5c5dcd0620942b82a2d238f3 --resource=kasko.zip --resource=kasko_symbols.zip --overwrite' in '/home/lqx/code/chromium'
INFO:get_syzygy_binaries.py:Unexpected output directory, skipping cleanup.

>________ running 'download_from_google_storage --no_resume --platform=win32 --directory --recursive --no_auth --num_threads=16 --bucket chromium-apache-win32 src/third_party/apache-win32' in '/home/lqx/code/chromium'
The current platform doesn't match "win32", skipping.

>________ running 'download_from_google_storage --no_resume --platform=linux* --extract --no_auth --bucket chromium-fonts -s src/third_party/blimp_fonts/font_bundle.tar.gz.sha1' in '/home/lqx/code/chromium'
0> Downloading src/third_party/blimp_fonts/font_bundle.tar.gz...
0> Extracting 203 entries from src/third_party/blimp_fonts/font_bundle.tar.gz to src/third_party/blimp_fonts/font_bundle
Success!
Downloading 1 files took 1100.837104 second(s)
Hook 'download_from_google_storage --no_resume '--platform=linux*' --extract --no_auth --bucket chromium-fonts -s src/third_party/blimp_fonts/font_bundle.tar.gz.sha1' took 1100.90 secs

>________ running '/usr/bin/python src/third_party/instrumented_libraries/scripts/download_binaries.py' in '/home/lqx/code/chromium'

>________ running '/usr/bin/python src/build/gyp_chromium' in '/home/lqx/code/chromium'
Updating projects from gyp files...
Hook '/usr/bin/python src/build/gyp_chromium' took 115.37 secs

[e] 使用 www.example.org 出现的认证问题，quic的部分日志
* quic_server的部分日志
>[0324/185905:VERBOSE1:quic_connection.cc(2105)] Entering Batch Mode.
[0324/185905:VERBOSE1:quic_packet_creator.cc(519)] Adding frame: type { STREAM_FRAME } stream_id { 1 } fin { 0 } offset { 0 } length { 1325 }
[0324/185905:VERBOSE1:quic_framer.cc(645)] Appending header: { connection_id: 18126346989608483412, connection_id_length:8, packet_number_length:1, multipath_flag: 0, reset_flag: 0, version_flag: 0, fec_flag: 0, entropy_flag: 1, entropy hash: 0, path_id: , packet_number: 1, is_in_fec_group:0, fec_group: 0}
[0324/185905:VERBOSE1:quic_connection.cc(1517)] Server: Sending packet 1 : data bearing , encryption level: ENCRYPTION_NONE, encrypted length:1350
[0324/185905:VERBOSE1:quic_connection.cc(1563)] Server: time we began writing last sent packet: 794574320
[0324/185905:VERBOSE1:quic_packet_creator.cc(519)] Adding frame: type { STREAM_FRAME } stream_id { 1 } fin { 0 } offset { 1325 } length { 21 }
[0324/185905:VERBOSE1:quic_packet_creator.cc(519)] Adding frame: type { PADDING_FRAME } 
[0324/185905:VERBOSE1:quic_framer.cc(645)] Appending header: { connection_id: 18126346989608483412, connection_id_length:8, packet_number_length:1, multipath_flag: 0, reset_flag: 0, version_flag: 0, fec_flag: 0, entropy_flag: 1, entropy hash: 0, path_id: , packet_number: 2, is_in_fec_group:0, fec_group: 0}
[0324/185905:VERBOSE1:quic_connection.cc(1517)] Server: Sending packet 2 : data bearing , encryption level: ENCRYPTION_NONE, encrypted length:1350
[0324/185905:VERBOSE1:quic_connection.cc(1563)] Server: time we began writing last sent packet: 794574518
[0324/185905:VERBOSE1:quic_connection.cc(2138)] Leaving Batch Mode.
[0324/185905:VERBOSE1:quic_flow_controller.cc(88)] Server: Stream 1 sent: 1346
[0324/185905:VERBOSE1:stream_sequencer_buffer.cc(56)] Retired block with index: 0
[0324/185905:VERBOSE1:stream_sequencer_buffer.cc(438)] Removed FrameInfo with offset: 0 and length: 1300
[0324/185905:VERBOSE1:quic_flow_controller.cc(50)] Server: Stream 1 consumed: 1300
[0324/185905:VERBOSE1:quic_flow_controller.cc(178)] Server: Not sending WindowUpdate for stream 1, available window: 64236 >= threshold: 32768
[0324/185905:VERBOSE1:quic_connection.cc(912)] Server: Got packet 1 for 18126346989608483412
[0324/185905:VERBOSE1:quic_connection.cc(2105)] Entering Batch Mode.
[0324/185905:VERBOSE1:quic_connection.cc(2138)] Leaving Batch Mode.
[0324/185905:WARNING:quic_framer.cc(562)] Unable to process packet header.  Stopping parsing.
[0324/185905:VERBOSE1:quic_connection.cc(1357)] Server: time of last received packet: 794592436
[0324/185905:VERBOSE1:quic_connection.cc(632)] Server: Received packet header: { connection_id: 18126346989608483412, connection_id_length:8, packet_number_length:1, multipath_flag: 0, reset_flag: 0, version_flag: 0, fec_flag: 0, entropy_flag: 1, entropy hash: 4, path_id: , packet_number: 2, is_in_fec_group:0, fec_group: 0}
[0324/185905:VERBOSE1:quic_connection.cc(666)] Server: OnAckFrame: entropy_hash: 6 largest_observed: 2 ack_delay_time: 13944 missing_packets: [  ] is_truncated: 0 received_packets: [ 1 at 794583166 2 at 794585336  ]
[0324/185905:VERBOSE1:quic_sent_packet_manager.cc(320)] Server: Got an ack for packet 1
[0324/185905:VERBOSE1:quic_sent_packet_manager.cc(320)] Server: Got an ack for packet 2
[0324/185905:VERBOSE1:hybrid_slow_start.cc(52)] Reset hybrid slow start @2
[0324/185905:VERBOSE1:quic_sustained_bandwidth_recorder.cc(38)] Started recording at: 794592436
[0324/185905:VERBOSE1:quic_connection.cc(912)] Server: Got packet 2 for 18126346989608483412
[0324/185905:VERBOSE1:quic_connection.cc(2105)] Entering Batch Mode.
[0324/185905:VERBOSE1:quic_connection.cc(2138)] Leaving Batch Mode.
[0324/185905:VERBOSE1:quic_connection.cc(1357)] Server: time of last received packet: 794593473
[0324/185905:VERBOSE1:quic_connection.cc(632)] Server: Received packet header: { connection_id: 18126346989608483412, connection_id_length:8, packet_number_length:1, multipath_flag: 0, reset_flag: 0, version_flag: 0, fec_flag: 0, entropy_flag: 0, entropy hash: 0, path_id: , packet_number: 3, is_in_fec_group:0, fec_group: 0}
[0324/185905:VERBOSE1:quic_connection.cc(666)] Server: OnAckFrame: entropy_hash: 6 largest_observed: 2 ack_delay_time: 15016 missing_packets: [  ] is_truncated: 0 received_packets: [ 1 at 794583166 2 at 794585336  ]
[0324/185905:VERBOSE1:quic_sustained_bandwidth_recorder.cc(56)] New max bandwidth estimate (KBytes/s): 11756
[0324/185905:VERBOSE1:quic_connection.cc(842)] Server: CONNECTION_CLOSE_FRAME received for connection: 18126346989608483412 with error: QUIC_PROOF_INVALID Proof invalid: Failed to verify certificate chain: net::ERR_CERT_COMMON_NAME_INVALID
[0324/185905:VERBOSE1:quic_dispatcher.cc(305)] Closing connection (18126346989608483412) due to error: QUIC_PROOF_INVALID
[0324/185905:VERBOSE1:quic_dispatcher.cc(333)] Connection 18126346989608483412 added to time wait list.
[0324/185905:VERBOSE1:quic_framer.cc(1152)] Visitor asked to stop further processing.

* quic_client的部分日志
>[0324/185905:VERBOSE1:quic_crypto_client_stream.cc(418)] Reasons for rejection: 2048
[0324/185905:VERBOSE1:proof_verifier_chromium.cc(418)] VerifyFinal success
[0324/185905:VERBOSE1:quic_crypto_client_stream.cc(474)] Doing VerifyProof
[0324/185905:VERBOSE1:stream_sequencer_buffer.cc(56)] Retired block with index: 0
[0324/185905:VERBOSE1:stream_sequencer_buffer.cc(438)] Removed FrameInfo with offset: 1325 and length: 21
[0324/185905:VERBOSE1:quic_flow_controller.cc(50)] Client: Stream 1 consumed: 1346
[0324/185905:VERBOSE1:quic_flow_controller.cc(178)] Client: Not sending WindowUpdate for stream 1, available window: 15038 >= threshold: 8192
[0324/185905:VERBOSE1:quic_connection.cc(912)] Client: Got packet 2 for 18126346989608483412
[0324/185905:VERBOSE1:quic_connection.cc(2105)] Entering Batch Mode.
[0324/185905:VERBOSE1:quic_connection.cc(2109)] Bundling ack with outgoing packet.
[0324/185905:VERBOSE1:quic_packet_creator.cc(519)] Adding frame: type { ACK_FRAME } entropy_hash: 6 largest_observed: 2 ack_delay_time: 13946 missing_packets: [  ] is_truncated: 0 received_packets: [ 1 at 794576003 2 at 794578173  ]
[0324/185905:VERBOSE1:quic_packet_creator.cc(519)] Adding frame: type { STOP_WAITING_FRAME } entropy_hash: 0 least_unacked: 1
[0324/185905:VERBOSE1:quic_connection.cc(2138)] Leaving Batch Mode.
[0324/185905:VERBOSE1:quic_framer.cc(645)] Appending header: { connection_id: 18126346989608483412, connection_id_length:8, packet_number_length:1, multipath_flag: 0, reset_flag: 0, version_flag: 0, fec_flag: 0, entropy_flag: 1, entropy hash: 0, path_id: , packet_number: 2, is_in_fec_group:0, fec_group: 0}
[0324/185905:VERBOSE1:quic_connection.cc(1517)] Client: Sending packet 2 :  ack only , encryption level: ENCRYPTION_NONE, encrypted length:40
[0324/185905:VERBOSE1:quic_connection.cc(1563)] Client: time we began writing last sent packet: 794592264
[0324/185905:WARNING:proof_verifier_chromium.cc(344)] Failed to verify certificate chain: net::ERR_CERT_COMMON_NAME_INVALID
[0324/185905:VERBOSE1:quic_connection.cc(1876)] Client: Force closing 18126346989608483412 with error QUIC_PROOF_INVALID (42) Proof invalid: Failed to verify certificate chain: net::ERR_CERT_COMMON_NAME_INVALID
[0324/185905:VERBOSE1:quic_connection.cc(2105)] Entering Batch Mode.
[0324/185905:VERBOSE1:quic_connection.cc(2109)] Bundling ack with outgoing packet.
[0324/185905:VERBOSE1:quic_packet_creator.cc(519)] Adding frame: type { ACK_FRAME } entropy_hash: 6 largest_observed: 2 ack_delay_time: 15018 missing_packets: [  ] is_truncated: 0 received_packets: [ 1 at 794576003 2 at 794578173  ]
[0324/185905:VERBOSE1:quic_packet_creator.cc(519)] Adding frame: type { STOP_WAITING_FRAME } entropy_hash: 0 least_unacked: 1
[0324/185905:VERBOSE1:quic_packet_creator.cc(519)] Adding frame: type { CONNECTION_CLOSE_FRAME } error_code { 42 } error_details { Proof invalid: Failed to verify certificate chain: net::ERR_CERT_COMMON_NAME_INVALID }
[0324/185905:VERBOSE1:quic_framer.cc(645)] Appending header: { connection_id: 18126346989608483412, connection_id_length:8, packet_number_length:1, multipath_flag: 0, reset_flag: 0, version_flag: 0, fec_flag: 0, entropy_flag: 0, entropy hash: 0, path_id: , packet_number: 3, is_in_fec_group:0, fec_group: 0}
[0324/185905:VERBOSE1:quic_connection.cc(1517)] Client: Sending packet 3 : data bearing , encryption level: ENCRYPTION_NONE, encrypted length:131
[0324/185905:VERBOSE1:quic_connection.cc(1563)] Client: time we began writing last sent packet: 794593396
[0324/185905:VERBOSE1:quic_connection.cc(2138)] Leaving Batch Mode.
Failed to connect to 127.0.0.1:6121. Error: QUIC_PROOF_INVALID
