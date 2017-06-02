# linux commands

## find

```shell
find /log/ -name '*.log' -newermt '2013-08-08' ! -newermt '2013-09-09'
find /log/ -name '*.log' -not -name '2013-09-09*.log'
```
http://www.jb51.net/LINUXjishu/182748.html
