Title: 在联想G450上安装无线驱动网卡(Debian7.8)
Date: 2015-06-06 22:16
Tags: debian, linux
Author: woniu17
Summary: 在联想G450上安装无线驱动网卡(Debian7.8)

## 主要步骤：

1. 下载驱动
2. 编译源码
3. 移除冲突驱动模块
4. 加载模块
5. 禁止

## 详细步骤：

### 下载驱动
    
### 编译源码
  ```
  $su
  #make clean
  #make
  #ls #可以看到生成文件wl.ko
  #make API=WEXT
  ```
### 移除冲突驱动模块
  ```
  #rmmod b43
  #rmmod ssb
  #rmmod bcma
  #rmmod wl
  ```
### 加载模块
  ```
  #modprobe lib89211
  #insmod wl.ko
  #depmod -a
  ```
### 禁止
