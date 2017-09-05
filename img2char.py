# -*- coding: utf-8 -*-

char_string = 'abcdefghipqrstuvwxyz'
char_string = '"$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!;:,\"^`\'.\"'
char_string = '2emo'
html_head = '''
<!DOCTYPE html>
<html>
<head>
<style>
div
{
width:0px;
height:0px;
}
div#image
{
margin:0px;
transform:scale(0.2,0.2);
-ms-transform:scale(0.2,0.2); /* IE 9 */
-moz-transform:scale(0.2,0.2); /* Firefox */
-webkit-transform:scale(0.2,0.2); /* Safari and Chrome */
-o-transform:scale(0.2,0.2); /* Opera */
}
</style>
<script type="text/javascript">
var i = 20;
function hello() {
	i = i - 0.1;
	var s = "scale(" + i + ")";
	document.getElementById("image").style.Transform=s;
	document.getElementById("image").style.WebkitTransform=s;
	document.getElementById("image").style.msTransform=s;
	document.getElementById("image").style.MozTransform=s;
	document.getElementById("image").style.oTransform=s;
	if (i > 0.2) {
		window.setTimeout(hello, 5);
	}
}
window.onload=hello
</script>
</head>
<body>
<div id="image">
<code>
'''
html_tail = '''
</code>
</div>
</body>
</html>
'''

def rgb2char(r, g, b):
    length = len(char_string)
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)

    # 每个字符对应的gray值区间宽度
    unit = (256.0 + 1) / length

    # gray值对应到char_string中的位置（索引值）
    idx = int(gray / unit)
    return char_string[idx]

from PIL import Image

#预处理（将图片尺寸压缩，并转为灰度图）
def preprocess(img_path, delta=100):
    img = Image.open(img_path)
    # 获取图片尺寸
    width, height = img.size

    # 伸缩倍数scale
    scale = 4
    width, height = int(width / scale * 3.0), int(height / scale)
    img = img.resize((width, height))
    return img

def img2char(img_obj, savepath):
    html = html_head
    width, height = img_obj.size
    # 获取像素点的rgb元组值，如(254, 0, 0)，并将其转化为字符
    for i in range(height):
        line = ''
        for j in range(width):
            line += rgb2char(*img_obj.getpixel((j, i)))
        html = html + line + '\n'

    html = html + html_tail
    # 保存字符画
    with open(savepath, 'w+') as f:
        f.write(html)


img_path = './a.jpg'
savepath = './a.html'
img_obj = preprocess(img_path, 10)
img2char(img_obj, savepath)
