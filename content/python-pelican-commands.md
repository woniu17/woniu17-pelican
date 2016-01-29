Title: Pelican使用
Date: 2016-01-29 14:02
Category: Pelican
Tags: pelican
Author: qingluck
Slug: pelican
Summary: Pelican的使用

### 创建一个新博客

```bash
mkdir -p /path/to/myblog
cd /path/to/myblog
```

### 写文章

```bash
vi /path/to/myblog/content/article.md
```

### 生成html

```bash
cd /path/to/myblog
make html
```

### 本地运行测试

```bash
cd /path/to/myblog
./develop_server.sh start
```

使用浏览器访问`http://localhost:8000`


### 关闭本地运行

```bash
cd /path/to/myblog
./develop_server.sh stop
```
