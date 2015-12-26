Title: Git中的submodule命令
Date: 2015-12-26 14:12
Category: Git
Tag: git
Author: woniu17
Summary: Git中的`submodule`命令

本文链接：[Git中的`submodule`命令]({filename}/git-submodule.md)

本文以代码库[https://github.com/woniu17/woniu17-pelican](https://github.com/woniu17/woniu17-pelican){:target="_blank"}为例,
说明Git中`submodule`命令的使用
该代码库中包含子模块`pelican-themes/niu-x2-sidebar`, `pelican-plugin`以及`publish`，每个子模块实际上是一个代码库，
由该代码库中的`.gitmodules`文件中的内容可以看出:
```
[submodule "pelican-themes/niu-x2-sidebar"]
    path = pelican-themes/niu-x2-sidebar
    url = https://github.com/qingtech/niu-x2-sidebar.git
[submodule "pelican-plugins"]
    path = pelican-plugins
    url = https://github.com/qingtech/pelican-plugins.git
[submodule "publish"]
    path = publish
    url = https://github.com/woniu17/woniu17.github.io.git
```

### clone带有子模块的代码库

#### 下载主代码库

```bash
git clone https://github.com/woniu17/woniu17/woniu17-pelican.git
```

#### 进入代码库的主目录

```bash
cd woniu17-pelican
```

#### 下载该代码库中的所有子模块

```bash
git submodule update --init --recursive
```

### 添加子模块`publish-for-gitcafe`

#### 在代码库的主目录下执行以下命令：

```bash
git submodule add https://gitcafe.com/woniu17/woniu17-pelican.git publish-for-gitcafe
```

上述命令会在`.gitmodules`文件添加以下内容，并会将子模块代码库克隆到publish-for-gitcafe目录下
```
[submodule "publish-for-gitcafe"]
    path = publish-for-gitcafe
    url = https://gitcafe.com/woniu17/woniu17-pelican.git
```

### 删除子模块`publish-for-gitcafe`
#### 将`.gitmodules`文件中的相关内容删除，即删除以下几行内容:
```
[submodule "publish-for-gitcafe"]
    path = publish-for-gitcafe
    url = https://gitcafe.com/woniu17/woniu17-pelican.git
```

#### 在代码库主目录下执行以下命令：

```bash
git rm --cached publish-for-gitcafe
```

#### 删除目录`publish-for-gitcafe`

```bash
rm -rf publish-for-gitcafe`
```

本文参考：[http://blog.csdn.net/wangjia55/article/details/24400501](http://blog.csdn.net/wangjia55/article/details/24400501){:target="_blank"}
