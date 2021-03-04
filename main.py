import math
import os
import requests
from waveshare_epd import epd2in9b_V3
from PIL import Image, ImageDraw, ImageFont


def main(sleep=True, clear=False):
    # Get data from pi-hole
    data = get_data("http://192.168.0.5/admin/api.php")
    # Initialize Display
    display = epd2in9b_V3.EPD()
    if sleep:
        display.init()
    if clear:
        display.Clear()
    # Fonts
    font_logo = ImageFont.truetype(os.path.join(os.getcwd(), 'Font.ttc'), 40)
    font_large = ImageFont.truetype(os.path.join(os.getcwd(), 'Font.ttc'), 24)
    font_small = ImageFont.truetype(os.path.join(os.getcwd(), 'Font.ttc'), 12)
    # Draw
    black_image = Image.new('1', (display.height, display.width), 255)
    red_image = Image.new('1', (display.height, display.width), 255)
    draw_black = ImageDraw.Draw(black_image)
    draw_red = ImageDraw.Draw(red_image)
    draw_black.text((0, 0), "Pi-hole", font=font_logo, fill=0)
    draw_black.text(
        (0, 40),
        "Queries: " + str(data['queries']),
        font=font_large,
        fill=0,
    )
    draw_red.text(
        (0, 65),
        "Blocked: " + str(data["blocked"]) + " (" + str(data["percentage_blocked"]) + "%)",
        font=font_large,
        fill=0,
    )
    draw_black.text(
        (0, 110),
        "Clients: " + str(data["clients"]) + " | Blocked Domains: " + str(data["blocked_domains"]) + " |",
        font=font_small,
        fill=0,
    )
    if data["enabled"]:
        draw_black.text((220, 110), "Online", font=font_small, fill=0)
    else:
        draw_red.text((220, 110), "Offline!", font=font_small, fill=0)
    # Add logo
    logo = Image.open('logo.bmp')
    logo.thumbnail((50, 50), resample=Image.HAMMING)
    black_image.paste(logo, (display.height - 50, 0), mask=logo.split()[-1])
    red_image.paste(logo.split()[1], (display.height - 50, 0), mask=logo.split()[-1])
    # Draw on display
    display.display(display.getbuffer(black_image), display.getbuffer(red_image))
    if sleep:
        display.sleep()


def get_data(url):
    response = requests.get(url)
    data = response.json()
    return {
        "queries": data["dns_queries_today"],
        "blocked": data["ads_blocked_today"],
        "percentage_blocked": math.floor(data["ads_percentage_today"] * 10) / 10,
        "clients": data["unique_clients"],
        "blocked_domains": data["domains_being_blocked"],
        "enabled": data["status"] == "enabled",
    }

if __name__ == "__main__":
    main()
