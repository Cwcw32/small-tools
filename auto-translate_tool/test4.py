# 获取图片base64测试
from PIL import Image
img = Image.open("jietu.jpg")

import base64

with open("jietu.jpg", 'rb') as f:
    base64_data = base64.b64encode(f.read())
    s = base64_data.decode()
    print(s)


