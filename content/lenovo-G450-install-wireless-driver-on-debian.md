Title: 在联想G450上安装无线驱动网卡(Debian7.8)
Date: 2015-06-06 22:16
Category: Linux
Tags: debian, linux
Author: woniu17
Summary: 在联想G450上安装无线驱动网卡(Debian7.8 32-bit)

本文链接：[在联想G450上安装无线驱动网卡(Debian7.8 32-bit)]({filename}/lenovo-G450-install-wireless-driver-on-debian.md)


## 步骤概述：

1. 下载驱动
2. 编译源码
3. 将wl.ko复制到系统模块文件相应的位置
4. 禁止加载冲突驱动模块
5. 更新初始化内存盘镜像initrd.img
6. 重启电脑，使模块加载更改生效

## 详细步骤：

### 下载驱动
  在[http://www.broadcom.com/support/?gid=1](http://www.broadcom.com/support/?gid=1){:target="_blank"}
  选择`Linuxi STA 32-bit driver`(如果是64位系统，选择相应版本)下载到`~/Download`文件夹
  进入`~/Download`文件夹，解压该文件`hybrid-v35-nodebug-pcoem-6_30_223_248.tar.gz`
```bash
  user@debian:~$ cd ~/Download
  user@debian:~/Download$ mkdir wlan
  user@debian:~/Download$ tar -zxvf hybrid-v35-nodebug-pcoem-6_30_223_248.tar.gz -C wlan
  user@debian:~/Download/wlan$ cd wlan
  user@debian:~/Download/wlan$ ls
```
  可以看到`wlan`文件夹下有`Makefile`文件，`src`和`lib`两个文件夹

### 编译源码
```bash
  user@debian:~/Download/wlan$ make clean
  user@debian:~/Download/wlan$ make #或者make API=WEXT
  user@debian:~/Download/wlan$ ls 
```
  可以看到生成wl.ko等文件

### 将wl.ko复制到系统模块文件相应的位置
```bash
  user@debian:~/Download/wlan$ su #切换到root用户
  root@debian:/home/user/Download/wlan# cp wl.ko /lib/modules/`uname -r`/kernel/drivers/net/wireless
```
  注意 *\`uname -r\`* 中的点是ESC键下面的那个键，该命令是获取内核版本，
  本次操作中的内核版本为3.2.0-4-686-pae，
  这里可以直接写内核的版本号。

### 禁止加载冲突驱动模块
```bash
  root@debian:/home/user/Download/wlan# echo "blacklist ssb" >> /etc/modprobe.d/blacklist.conf
  root@debian:/home/user/Download/wlan# echo "blacklist b43" >> /etc/modprobe.d/blacklist.conf
  root@debian:/home/user/Download/wlan# echo "blacklist bcma" >> /etc/modprobe.d/blacklist.conf
```

### 更新初始化内存盘镜像initrd.img
```bash
  root@debian:/home/user/Download/wlan# update-initramfs -u
```

### 重启电脑，使模块加载更改生效，此时G450可以通过无线网卡上网了！

---
### 参考文献
- [http://wenku.baidu.com/view/171ac6afd1f34693daef3efc.html](http://wenku.baidu.com/view/171ac6afd1f34693daef3efc.html){:target="_blank"}
- [https://wiki.debian.org/KernelModuleBlacklisting](https://wiki.debian.org/KernelModuleBlacklisting){:target="_blank"}

