import math
import os

from api import PiHoleAPI

import epaper
from PIL import Image, ImageDraw, ImageFont


def main(sleep=True, clear=False):
    # Get data from pi-hole
    api = PiHoleAPI()
    data = api.get_stats()
    # Initialize Display
    display = epaper.epaper("2in9b_V3").EPD()
    if sleep:
        display.init()
    if clear:
        display.Clear()
    # Fonts
    font_logo = ImageFont.truetype(os.path.join(os.getcwd(), "Font.ttc"), 40)
    font_large = ImageFont.truetype(os.path.join(os.getcwd(), "Font.ttc"), 24)
    font_small = ImageFont.truetype(os.path.join(os.getcwd(), "Font.ttc"), 12)
    # Draw
    black_image = Image.new("1", (display.height, display.width), 255)
    red_image = Image.new("1", (display.height, display.width), 255)
    draw_black = ImageDraw.Draw(black_image)
    draw_red = ImageDraw.Draw(red_image)
    draw_black.text((0, 0), "Pi-hole", font=font_logo, fill=0)
    draw_black.text(
        (0, 40),
        "Queries: " + str(data["queries"]["total"]),
        font=font_large,
        fill=0,
    )
    draw_red.text(
        (0, 65),
        "Blocked: "
        + str(data["queries"]["blocked"])
        + " ("
        + str(data["queries"]["percentage_blocked"])
        + "%)",
        font=font_large,
        fill=0,
    )
    draw_black.text(
        (0, 110),
        "Clients: " + str(data["clients"]["active"]) + " | Requests/Second: ",
        +str(data["queries"]["frequency"]),
        font=font_small,
        fill=0,
    )
    # Add logo
    logo = Image.open("logo.bmp")
    logo.thumbnail((50, 50), resample=Image.HAMMING)
    black_image.paste(logo, (display.height - 50, 0), mask=logo.split()[-1])
    red_image.paste(logo.split()[1], (display.height - 50, 0), mask=logo.split()[-1])
    # Draw on display
    display.display(display.getbuffer(black_image), display.getbuffer(red_image))
    if sleep:
        display.sleep()


if __name__ == "__main__":
    main()
