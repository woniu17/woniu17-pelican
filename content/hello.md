Title: Hello, world!
Date: 2015-05-29 19:54
Category: Pelican
Tags: pelican, markdown
Slug: hello
Author: qingluck
Summary: Hello pelican and markdown.
Comment: off

## Hello pelican and markdown.

### My home page is [www.linqingxiang.com](http://www.linqingxiang.com)

------

### *python*[^python] **学习**

> The Zen of Python, by Tim Peters
>
> Beautiful is better than ugly.
> Explicit is better than implicit.
> Simple is better than complex.
> Complex is better than complicated.
> Flat is better than nested.
> Sparse is better than dense.
> Readability counts.
> Special cases aren't special enough to break the rules.
> Although practicality beats purity.
> Errors should never pass silently.
> Unless explicitly silenced.
> In the face of ambiguity, refuse the temptation to guess.
> There should be one-- and preferably only one --obvious way to do it.
> Although that way may not be obvious at first unless you're Dutch.
> Now is better than never.
> Although never is often better than *right* now.
> If the implementation is hard to explain, it's a bad idea.
> If the implementation is easy to explain, it may be a good idea.
> Namespaces are one honking great idea -- let's do more of those!

```python
def hello():
    print 'hello, python!'

if __name__ == '__main__' :
    hello()
```

### LaTeX[^latex]公式
- 行内公式：$Gamma(n) = (n-1)!\quad\forall n\in\mathbb N$
- 块级公式：

$$ x = \dfrac{-b \pm \sqrt{b^2 -4ac}}{2a} $$


### 表格

| Tables        | Are           | Cool  |
| ------------- |:-------------:| -----:|
| col 3 is      | right-aligned | $1600 |
| col 2 is      | centered      |   $12 |
| zebra stripes | are neat      |    $1 |

### 流程图
```flow
st=>start: Start
e=>end
op=>operation: My Operation
cond=>condition: Yes or No?

st->op->cond
cond(yes)->e
cond(no)->op
```

### 时序图:

```sequence
Alice->Bob: Hello Bob, how are you?
Note right of Bob: Bob thinks
Bob-->Alice: I am good thanks!
```

### TODO-list
- [x] todo item x
- [ ] todo item y
- [ ] todo item z

### 快捷键

- 帮助    `Ctrl + /`
- 同步文档    `Ctrl + S`
- 创建文档    `Ctrl + Alt + N`
- 最大化编辑器    `Ctrl + Enter`
- 预览文档 `Ctrl + Alt + Enter`
- 文档管理    `Ctrl + O`
- 系统菜单    `Ctrl + M` 

[^python]:  是一种面向对象、解释型计算机程序设计语言，由Guido van Rossum于1989年底发明，第一个公开发行版发行于1991年，Python 源代码同样遵循 GPL(GNU General Public License)协议。[详情](http://baike.baidu.com/view/21087.htm){:target="_blank"}
[^latex]: 是一种基于ΤΕΧ的排版系统，由美国计算机学家莱斯利·兰伯特（Leslie Lamport）在20世纪80年代初期开发。[详情](http://baike.baidu.com/view/769333.htm){:target="_blank"}
