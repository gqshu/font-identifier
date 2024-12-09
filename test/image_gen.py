import random

from PIL import Image, ImageDraw, ImageFont

font_size = 25
text = "你好"
font_path = "C:\\Windows\\Fonts\\msyh.ttc"
font = ImageFont.truetype(font_path, font_size, index=0)

img = Image.new('RGB', (800, 400), color="white")  # Canvas size
draw = ImageDraw.Draw(img)

# Random offsets, but ensuring that text isn't too far off the canvas
offset_x = random.randint(0, 100)
offset_y = random.randint(0, 100)

print('draw.')
# vary the line height
line_height = random.uniform(0, 1.25) * font_size
print(line_height, offset_x, offset_y)
draw.text((offset_x, offset_y), text, fill="black", font=font)
print("draw done.")

img.show()
print("show.")
img.save('test_1.png')
