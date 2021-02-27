from waveshare_epd import epd2in9b_V3
from PIL import Image, ImageDraw, ImageFont

# Initialize Display
display = epd2in9b_V3.EPD()
display.init()
display.Clear()

# Fonts
font_24 = ImageFont.truetype(os.path.join(os.getcwd(), 'Font.ttc'), 24)

# Draw
border_box = Image.new('1', (display.height, display.width), 255)
draw_black = ImageDraw.Draw(border_box)
drawblack.text((10, 0), '', font=font_24, fill=0)
display.display(display.getbuffer(border_box), None)
