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

### *python* **学习**

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

### LaTeX公式
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
