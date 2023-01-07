from PIL import ImageDraw, ImageFont, Image


def draw_text(image, text, position):
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("assets/cursive.ttf", 70)
    w, h = draw.textsize(text, font=font)

    position = position[0] - w / 2, position[1] - h / 2
    black = (0, 0, 0)

    draw.text(position, text, black, font=font, align="right")

    return image


names = ["Rohit", "Sunith"]

for name in names:
    img = Image.open("assets/certificate.jpg")
    draw_text(img, name, (650, 520))
    img.save(f"{name}.jpg")

